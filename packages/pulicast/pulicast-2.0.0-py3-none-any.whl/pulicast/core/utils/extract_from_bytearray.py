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


def extract(data: bytearray, fmt: str):
    size = struct.calcsize(fmt)
    if size > len(data):
        return None
    v = struct.unpack(fmt, data[:size])
    del data[:size]
    return v[0]


def extract_uint8(data: bytearray) -> int:
    return extract(data, 'B')


def extract_uint32(data: bytearray) -> int:
    return extract(data, '!I')


def extract_string(data: bytearray, size: int) -> str:
    if size > len(data):
        return None
    v = data[:size].decode("ascii")
    del data[:size]
    return v


