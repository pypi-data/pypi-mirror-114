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
from pulicast import Address


def test_socket_id_equality():
    # GIVEN
    # Two equal IDs
    id1 = Address(123, 123)
    id2 = Address(123, 123)

    # Two IDs distinct from the previous ones
    id3 = Address(1234, 123)
    id4 = Address(123, 1234)

    id5 = "NOT AN ID"

    # THEN
    assert id1 == id1
    assert id1 == id2

    assert id1 != id3
    assert id1 != id4
    assert id1 != id5


def test_socket_id_hash():
    id1 = Address(123, 123)
    id2 = Address(123, 123)

    id3 = Address(1234, 123)
    id4 = Address(123, 1234)

    assert hash(id3) != hash(id4)
    assert hash(id1) == hash(id2)
