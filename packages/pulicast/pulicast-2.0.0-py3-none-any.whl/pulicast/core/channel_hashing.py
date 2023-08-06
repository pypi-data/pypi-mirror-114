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
import ipaddress
from functools import reduce

MulticastGroup = str


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
