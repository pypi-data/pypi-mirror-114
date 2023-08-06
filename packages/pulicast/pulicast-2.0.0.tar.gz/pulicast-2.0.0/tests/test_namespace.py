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
from tests.utils.mock_node import make_mock_node

"""
Note: These tests assume the following channel structure:

 ├── drivers
 │   ├── rover1  (the node default namespace)
 │   │   ├── arm
 │   │   │   └── attitude
 │   │   └── attitude
 │   └── rover2
 │       ├── arm
 │       │   └── attitude
 │       └── attitude
 └── flyers  (the other_ns)
     ├── glider1
     │   ├── attitude
     │   └── flap
     │       └── angle
     └── glider2
         ├── attitude
         └── flap
             └── angle
"""


def test_that_namespace_ist_prepended_to_channel_name():
    # GIVEN
    node = make_mock_node("/drivers/rover1")
    other_ns = node.make_namespace("flyers/glider1")

    # THEN
    assert node["attitude"].name == "drivers/rover1/attitude"
    assert other_ns["attitude"].name == "flyers/glider1/attitude"


def test_that_relative_access_is_resolved():
    # GIVEN
    node = make_mock_node("/drivers/rover1")
    other_ns = node.make_namespace("flyers/glider1")

    # THEN
    assert (node / "arm")["attitude"].name == "drivers/rover1/arm/attitude"
    assert (other_ns / "flap")["angle"].name == "flyers/glider1/flap/angle"
    assert (other_ns / ".." / "glider2")["attitude"].name == "flyers/glider2/attitude"