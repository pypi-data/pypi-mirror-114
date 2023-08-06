#!/usr/bin/env python3
#     Copyright (C) 2021 Kiteswarms Ltd
#
#     This file is part of pulicast.
#
#     pulicast is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     pulicast is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with pulicast.  If not, see <https://www.gnu.org/licenses/>.
import selectors
import socket
import time
import warnings
from selectors import DefaultSelector
from typing import Callable, Dict, List, Optional

from pulicast import Address
from pulicast.core.transport import ChannelSender, Transport
from pulicast.transport.udp_transport import MAX_UDP_PACKET_SIZE, MulticastGroup, UDPChannelSender, \
    check_header_and_extract_channel_name, \
    multicast_group_for_channel, warn_about_invalid_interface_when_ttl_0


class PlainSocketChannelSender(UDPChannelSender):
    def __init__(self, channel_name: str, ttl: int, port: int, interface_address: Optional[str]):
        super().__init__(channel_name)
        self._group = multicast_group_for_channel(channel_name)
        self._port = port

        # ## Create Socket
        self._socket = sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # ## Set TTL
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        # TODO(max): set IP_TOS?
        # TODO(max): aaahhhh wy do we need this? Only this guy knows:
        # https://askubuntu.com/a/1243034/1180708
        if ttl == 0:
            join_multicast_group(self._socket, self._group, "0.0.0.0")

        # ## Set Loopback option
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        # ## Set Network Interface
        if interface_address is not None and interface_address != "0.0.0.0":
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(interface_address))

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF,
                        2 ** 16)  # TODO(max): determine the effect of this. Ref issue #13

        if ttl == 0 and not (interface_address is None or interface_address == "127.0.0.1"):
            warn_about_invalid_interface_when_ttl_0(interface_address)

    def send_to_socket(self, data: bytearray):
        self._socket.sendto(data, (self._group, self._port))

    def stop(self):
        self._socket.close()


class PlainSocketTransport(Transport):

    def __init__(self, port: int, ttl: int, interface_address: Optional[str]):
        # TODO(max): if TTL=0 then no if address should be set
        self._port = port
        self._ttl = ttl
        self._receive_sockets: List[socket] = []
        self._selector = DefaultSelector()
        self._interface_address = interface_address
        self.subscriptions_paused = False

        self._subscriptions: Dict[str, List[Callable[[bytearray, Address], None]]] = dict()

    def make_channel_sender(self, channel_name: str) -> ChannelSender:
        return PlainSocketChannelSender(channel_name, self._ttl, self._port, self._interface_address)

    def start_receiving_messages_for(self, channel_name: str, packet_callback: Callable[[bytearray, Address], None]):
        if channel_name not in self._subscriptions:
            self._subscriptions[channel_name] = []

        self._subscriptions[channel_name].append(packet_callback)
        self.join_multicast_group(multicast_group_for_channel(channel_name))

    def join_multicast_group(self, group: MulticastGroup):
        # Ensure we have at least one receive socket
        if self.num_open_sockets == 0:
            self._open_new_receive_socket()

        # Try to join the multicast group on the most recently generated receive socket and return on success
        try:
            join_multicast_group(self._receive_sockets[-1], group, self._interface_address)
        except Exception:
            # If joining failed, we open another socket
            self._open_new_receive_socket()

            try:
                # And try to join the new socket
                join_multicast_group(self._receive_sockets[-1], group, self._interface_address)
            except Exception as e:
                # only if the second attempt fails we report the error
                warnings.warn("Could not join multicast group on socket: " + str(e.args))

    @property
    def num_open_sockets(self):
        return len(self._receive_sockets)

    def _open_new_receive_socket(self):
        # ## Create Receiving Socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # ## Set Reuse Hints
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # ## Prevent receiving packets from all joined MC groups of this host
        if not hasattr(socket, 'IP_MULTICAST_ALL'):  # TODO: this is a hack right now
            socket.IP_MULTICAST_ALL = 49
        try:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_ALL, 0)
        except:
            pass

        # ## Binding to any address and the pulicast port
        sock.bind(("", self._port))  # Binding to the network interface only works with IP_ADD_MEMBERSHIP

        self._selector.register(sock, selectors.EVENT_READ)
        self._receive_sockets.append(sock)

    def handle_some(self, timeout=None):
        if self.num_open_sockets == 0 or self.subscriptions_paused:  # Workaround for https://bugs.python.org/issue29256
            time.sleep(timeout)
        else:
            for sock, mask in self._selector.select(timeout=timeout):
                data, address = sock.fileobj.recvfrom(MAX_UDP_PACKET_SIZE)
                self.handle_packet(bytearray(data), Address(*address))

    def stop(self):
        for s in self._receive_sockets:
            s.close()

    def handle_packet(self, data: bytearray, source: Address):
        channel_name = check_header_and_extract_channel_name(data)
        if channel_name is not None:
            for cb in self._subscriptions.get(channel_name, ()):
                cb(data, source)


def join_multicast_group(socket_handle, group: MulticastGroup, if_address: Optional[str]):
    socket_handle.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(group) +
                             (socket.inet_aton(if_address) if if_address is not None else b'\x00' * 4))

    # When listening on a specific interface that is not the loopback, join the group on the loopback
    # device too so that local messages are guaranteed to be delivered
    if if_address not in ("0.0.0.0", "127.0.0.1"):
        socket_handle.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                 socket.inet_aton(group) + socket.inet_aton("127.0.0.1"))
