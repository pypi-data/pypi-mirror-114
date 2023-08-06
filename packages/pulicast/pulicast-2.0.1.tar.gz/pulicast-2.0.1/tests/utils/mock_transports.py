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
from ipaddress import IPv4Address
from typing import Callable, Dict, List, Tuple, Optional

from pulicast import Address
from pulicast.channel import Channel
from pulicast.core.transport import ChannelSender, Transport


class MockChannelSender(ChannelSender):

    def __init__(self, channel_name: str, transport: 'MockTransport'):
        self._transport = transport
        self._channel_name = channel_name
        self.sent_packets: List[bytearray] = []

    def send(self, data: bytearray):
        self.sent_packets.append(data)
        self._transport.simulate_packet(data, self._transport.source_address, self._channel_name)


class MockTransport(Transport):

    def __init__(self):
        self.source_address = Address(123, 123)
        self.received_packets: List[Tuple[bytearray, Address]] = []
        self.subscriptions: Dict[str, List[Callable[[bytearray, Address], None]]] = dict()

    def make_channel_sender(self, channel_name: str) -> ChannelSender:
        return MockChannelSender(channel_name, self)

    def start_receiving_messages_for(self, channel_name: str, packet_callback: Callable[[bytearray, Address], None]):
        if channel_name not in self.subscriptions:
            self.subscriptions[channel_name] = []
        self.subscriptions[channel_name].append(packet_callback)

    def simulate_packet(self, packet: bytearray, source: Address, channel: str):
        self.received_packets.append((packet, source))
        for cb in self.subscriptions.get(channel, ()):
            cb(packet, source)


def make_channel_with_mock_transport(channel_name: str = "channel_name",
                                     mock_transport: Optional[MockTransport] = None) -> Tuple[Channel, MockTransport]:
    mock_transport = mock_transport if mock_transport else MockTransport()
    channel = Channel(channel_name, mock_transport)
    return channel, mock_transport
