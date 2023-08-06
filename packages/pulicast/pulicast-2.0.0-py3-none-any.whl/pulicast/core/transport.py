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
from typing import Callable

from pulicast import Address


class ChannelSender:
    def send(self, data: bytearray):
        raise NotImplementedError()


class Transport:
    def make_channel_sender(self, channel_name: str) -> ChannelSender:
        raise NotImplementedError()

    def start_receiving_messages_for(self, channel_name: str, packet_callback: Callable[[bytearray, Address], None]):
        raise NotImplementedError()
