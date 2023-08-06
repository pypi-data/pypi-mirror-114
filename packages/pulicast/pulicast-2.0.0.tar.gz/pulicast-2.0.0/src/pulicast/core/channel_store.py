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

from pulicast.channel import Channel
from pulicast.core.transport import Transport

from pulicast.core.utils.observable_dict import ObservableDict


class ChannelStore(ObservableDict[str, Channel]):
    """
    A container that holds :class:`.Channel` objects and lazily creates them on demand.
    """

    def __init__(self, transport: Transport):
        """
        :param transport: The :class:`.Transport` to pass on to newly created channels.
        """
        super().__init__()
        self._transport = transport

    def __getitem__(self, channel_name: str):
        """
        Returns the :class:`.Channel` object for the given channel name.

        If a channel object does not already exist, it will be created on demand.

        :param channel_name: The name of the channel.
        :return: A :class:`.Channel` object for the channel name.
        """
        channel = self.get(channel_name, None)
        if channel is None:
            channel = Channel(channel_name, self._transport)
            self[channel_name] = channel
        return channel
