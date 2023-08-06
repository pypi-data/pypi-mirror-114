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
import struct
import warnings
from typing import Optional

from pulicast.core.transport import ChannelSender
from pulicast.core.utils.extract_from_bytearray import extract_string, extract_uint8

PULICAST_PACKET_HEADER = b"PULI"

import ipaddress
from functools import reduce

MulticastGroup = str

MAX_UDP_PACKET_SIZE = 65507


def sdbm(L):
    """
    sdbm hash function for strings.

    .. note:: Has not been tested for speed.
    """
    return reduce(lambda h, c: ord(c) + (h << 6) + (h << 16) - h, L, 0)


def multicast_group_for_channel(channel_name: str) -> MulticastGroup:
    """
    Computes the multicast group that pulicast is going to use to publish messages on the given channel.

    .. note::
        As of now pulicast used the sdbm hash function to pseudo-randomly assign each channel a multicast group.
        This does not guarantee that all each channel is published on a unique multicast group.

    :param channel_name: The name of the channel on which to publish.
    :return: The multicast group on which to publish.
    """
    group = ipaddress.IPv4Address("239.0.0.0") + sdbm(channel_name) % int(2 ** 23)
    assert group.is_multicast
    assert not group.is_reserved
    return group.exploded


class UDPChannelSender(ChannelSender):

    def __init__(self, channel_name: str):
        self._channel_name = channel_name

    def send(self, data: bytearray):
        data = PULICAST_PACKET_HEADER + struct.pack("B", len(self._channel_name)) + self._channel_name.encode("ascii") + data
        self.send_to_socket(data)

    def send_to_socket(self, data: bytearray):
        raise NotImplementedError()


def check_header_and_extract_channel_name(data: bytearray) -> Optional[str]:
    """
    Will check that the header is equal to the pulicast header and extract the channel name form the packet.
    The data containing the header and channel name will be removed from the data.

    :param data: The bytes of the packet.
    :return: The channel name or None if the header did not match or there was a parsing error.
    """
    if data[:len(PULICAST_PACKET_HEADER)] != PULICAST_PACKET_HEADER:
        return None
    del data[:len(PULICAST_PACKET_HEADER)]

    channel_name_length = extract_uint8(data)
    if channel_name_length is None:
        return None

    channel_name = extract_string(data, channel_name_length)
    return channel_name


def warn_about_invalid_interface_when_ttl_0(interface):
    warnings.warn(f"When the TTL is 0 then packet can not leave the host and therefore "
                  f"specifying a network interface other than the loopback makes no sense."
                  f"Currently TTL is 0 and the network interface is {interface}!")
