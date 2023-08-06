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


class Address:
    """Identifies a socket using its IP and port number."""
    __slots__ = "ip", "port"

    def __init__(self, ip: int, port: int):
        self.ip = ip
        self.port = port

    def __hash__(self) -> int:
        return hash((self.ip, self.port))

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Address):
            return (self.ip, self.port) == (o.ip, o.port)
        else:
            return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __repr__(self) -> str:
        return f"ip: {self.ip}\tport: {self.port}"






