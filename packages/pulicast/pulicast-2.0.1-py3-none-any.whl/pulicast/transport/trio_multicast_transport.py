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
from typing import Callable, List, Optional
import socket as _stdlib_socket

import trio
from trio import socket
from socket import SO_REUSEADDR  # because trio does not expose it on Windows

from pulicast import Address
from pulicast.core.transport import ChannelSender, Transport
from pulicast.transport.plain_socket_transport import join_multicast_group
from pulicast.transport.udp_transport import MAX_UDP_PACKET_SIZE, MulticastGroup, UDPChannelSender, \
    check_header_and_extract_channel_name, \
    multicast_group_for_channel, warn_about_invalid_interface_when_ttl_0


class TrioChannelSender(UDPChannelSender):
    def __init__(self, channel_name: str, ttl: int, port: int, interface_address: Optional[str], nursery: trio.Nursery):
        super().__init__(channel_name)
        self._group = multicast_group_for_channel(channel_name)
        self._port = port

        # ## Create Socket
        self._socket = sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # ## Set TTL
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        # TODO(max): aaahhhh wy do we need this? Only this guy knows:
        #  https://askubuntu.com/a/1243034/1180708
        if ttl == 0:
            join_multicast_group(self._socket, self._group, "0.0.0.0")

        # ## Set Loopback option
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        # ## Set Network Interface
        if interface_address is not None and interface_address != "0.0.0.0":
            in_addr = socket.inet_aton(interface_address)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, in_addr)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF,
                        2 ** 16)  # TODO(max): determine the effect of this. Ref issue #13
        self._nursery = nursery

        if ttl == 0 and not (interface_address is None or interface_address == "127.0.0.1"):
            warn_about_invalid_interface_when_ttl_0(interface_address)

    def send_to_socket(self, data: bytearray):
        self._nursery.start_soon(self.async_send, data, self._group)

    async def async_send(self, packet: bytes, group: MulticastGroup):
        # This is the hacky but more performant version of the line. Might be solved better using sendmsg
        await self._socket._nonblocking_helper(
            _stdlib_socket.socket.sendto, [packet, (group, self._port)], {}, trio._core.wait_writable
        )
        # await self._get_socket().sendto(packet, (group, self._port))  #  this is not performant since it resolves the address again and again


class TrioMulticastTransport(Transport):
    def __init__(self, port: int, ttl: int, nursery: trio.Nursery, interface_address: Optional[str] = None):
        self._nursery = nursery
        self._interface_address = interface_address
        self._port = port
        self._ttl = ttl
        self._receive_sockets: List[trio.socket.socket] = []

    def make_channel_sender(self, channel_name: str) -> ChannelSender:
        return TrioChannelSender(channel_name, self._ttl, self._port, self._interface_address, self._nursery)

    def start_receiving_messages_for(self, channel_name: str, packet_callback: Callable[[bytearray, Address], None]):
        sock = trio.socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, SO_REUSEADDR, 1)
        if not hasattr(socket, 'IP_MULTICAST_ALL'):  # TODO: this is a hack right now
            socket.IP_MULTICAST_ALL = 49
        try:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_ALL, 0)
        except:  # TODO(max): why do we have this bare except here?
            pass

        # Binding to the network interface only works with the IP_ADD_MEMBERSHIP approach
        # Note: here we use the raw socket to bind to avoid an await sock.bind(...) which delays the subscription
        # for some time and can cause unexpected behaviour.
        sock._sock.bind(("", self._port))

        join_multicast_group(sock, multicast_group_for_channel(channel_name), self._interface_address)

        async def put_packets_to_channel():
            try:
                while True:

                    data, address = await sock.recvfrom(MAX_UDP_PACKET_SIZE)
                    data_bytes = bytearray(data)
                    received_channel_name = check_header_and_extract_channel_name(data_bytes)

                    if received_channel_name == channel_name:
                        source_address = Address(*address)
                        packet_callback(data_bytes, source_address)
            except trio.ClosedResourceError:
                pass

        self._nursery.start_soon(put_packets_to_channel)

        self._receive_sockets.append(sock)

    def stop(self):
        for s in self._receive_sockets:
            s.close()
