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

from pulicast.core.transport import ChannelSender


class SequenceNumberedSender:
    def __init__(self, channel_sender: ChannelSender):
        self._channel_sender = channel_sender
        self._seq_no = 0

    def send(self, data: bytearray):
        self._channel_sender.send(bytearray(struct.pack("!I", self.sequence_number)) + data)  # TODO: find more efficient way to do this
        self._seq_no += 1

    @property
    def sequence_number(self):
        return self._seq_no

