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
from pulicast.core.channel_store import ChannelStore
from pulicast.core.utils.name_resolution import resolve_name


class Namespace:
    """
    A pulicast namespace provides access to channels in a channel store relative to a given path.
    """

    def __init__(self, channel_store: ChannelStore, path: str = "/"):
        """
        Crates a new Namespace.

        :param channel_store: The channel store from which to retrieve the channels.
        :param path: The path relative to which the channels should be referred.
        """
        self._channel_store = channel_store
        self._path = path

    def __getitem__(self, channel_name: str) -> 'pulicast.Channel':
        return self._channel_store[resolve_name(channel_name, self._path)]

    def __truediv__(self, child: str):
        return Namespace(self._channel_store, resolve_name(child, self._path))

    def __str__(self):
        return self._path

    def __repr__(self):
        return str(self)

