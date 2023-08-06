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
import os
import warnings
from typing import Callable, List, Optional, Union

from PySide2.QtNetwork import QAbstractSocket, QHostAddress, QNetworkInterface, QUdpSocket

from pulicast import Address
from pulicast.core.transport import ChannelSender, Transport
from pulicast.transport.udp_transport import UDPChannelSender, check_header_and_extract_channel_name, \
    multicast_group_for_channel, warn_about_invalid_interface_when_ttl_0


def network_interface_from_address(address: Union[str, QHostAddress]) -> QNetworkInterface:
    address = QHostAddress(address)

    def addresses_of_interface(iface: QNetworkInterface):
        return (entry.ip() for entry in iface.addressEntries())

    interfaces_with_given_address = [ifc for ifc in QNetworkInterface.allInterfaces() if address in addresses_of_interface(ifc)]
    if len(interfaces_with_given_address) == 0:
        raise ValueError(f"The interface address {address.toString()} does not belong to any local network interface!")
    if len(interfaces_with_given_address) > 1:
        warnings.warn(f"There is more than one interface with the address {address.toString()}!"
                      f"{[ifc.name() for ifc in interfaces_with_given_address]}")
    return interfaces_with_given_address[0]


class QtChannelSender(UDPChannelSender):
    def __init__(self, channel_name: str, ttl: int, port: int, interface: Optional[QNetworkInterface] = None):
        super().__init__(channel_name)
        self._group = QHostAddress(multicast_group_for_channel(channel_name))
        self._port = port

        # ## Create Socket
        self._socket = QUdpSocket()
        # We need this bind to ensure we open an IPv4 socket and the MulticastTtlOption is properly set by QT
        self._socket.bind(QHostAddress(QHostAddress.AnyIPv4), 0)

        # ## Set TTL
        self._socket.setSocketOption(QAbstractSocket.MulticastTtlOption, ttl)
        #TODO(max): aaahhhh wy do we need this? Only this guy knows:
        # https://askubuntu.com/a/1243034/1180708
        if ttl == 0:
            self._socket.joinMulticastGroup(QHostAddress(self._group))

        # ## Set Loopback option
        self._socket.setSocketOption(QAbstractSocket.MulticastLoopbackOption, 1)

        # ## Set Network Interface
        if interface is not None:
            self._socket.setMulticastInterface(interface)

        if ttl == 0 and not (interface is None or interface.type() == QNetworkInterface.Loopback):
            warn_about_invalid_interface_when_ttl_0(interface)

    def send_to_socket(self, data: bytearray):
        self._socket.writeDatagram(data, self._group, self._port)


class QtTransport(Transport):

    def __init__(self, port: int, ttl: int, interface: Optional[Union[str, QNetworkInterface]] = None):
        self._port = port
        self._ttl = ttl
        self._receive_sockets: List[QUdpSocket] = []
        if interface is None:
            self._network_interface: Optional[QNetworkInterface] = None
        elif isinstance(interface, (QHostAddress, str)):
            self._network_interface = network_interface_from_address(interface)
        elif isinstance(interface, QNetworkInterface):
            self._network_interface = interface
        else:
            raise ValueError(f"Invalid network interface specification: {interface}!")

    def make_channel_sender(self, channel_name: str) -> ChannelSender:
        return QtChannelSender(channel_name, self._ttl, self._port, self._network_interface)

    def start_receiving_messages_for(self, channel_name: str, packet_callback: Callable[[bytearray, Address], None]):
        group = multicast_group_for_channel(channel_name)
        group_address = QHostAddress(group)
        sock = QUdpSocket()

        if os.name == 'posix':
            # Note: QT does not expose the IP_MULTICAST_ALL socket option. Therefore we use a new socket for each
            # multicast address that we join and bind it to the multicast address. This workaround is explained in
            # https://stackoverflow.com/a/2741989
            bind_successful = sock.bind(group_address, self._port,
                                        QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint)
            if not bind_successful:
                warnings.warn(f"Failed to bind to {group}. Falling back binding to {QHostAddress.AnyIPv4}."
                              f"This will trigger promiscuous mode where we receive all pulicast messages subscribed"
                              f"on this host and throw away the ones we don't need. Expect significant performance "
                              f"overhead!")
                bind_successful = sock.bind(QHostAddress(QHostAddress.AnyIPv4), self._port,
                                            QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint)
            if not bind_successful:
                warnings.warn(f"Failed to bind to a receiving socket: '{sock.error()}'. "
                              f"No pulicast messages can be received!")
                return
        elif os.name == 'nt':
            bind_successful = sock.bind(QHostAddress(QHostAddress.AnyIPv4), self._port,
                                        QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint)
            if not bind_successful:
                warnings.warn(f"Failed to bind to a receiving socket: '{sock.error()}'. "
                              f"No pulicast messages can be received!")
                return
        else:
            warnings.warn(f"Unsupported os: '{os.name}'")
            return

        if self._network_interface is None:
            sock.joinMulticastGroup(group_address)
        else:
            sock.joinMulticastGroup(group_address, self._network_interface)
            if self._network_interface.type() != QNetworkInterface.Loopback:
                sock.joinMulticastGroup(group_address, network_interface_from_address("127.0.0.1"))

        def read_datagram():
            while sock.hasPendingDatagrams():
                datagram = sock.receiveDatagram()
                data = bytearray(datagram.data().data())

                received_channel_name = check_header_and_extract_channel_name(data)

                if received_channel_name == channel_name:
                    source_address = Address(datagram.senderAddress().toIPv4Address(), datagram.senderPort())
                    packet_callback(data, source_address)

        sock.readyRead.connect(read_datagram)
        self._receive_sockets.append(sock)

    def stop(self):
        for s in self._receive_sockets:
            s.close()
