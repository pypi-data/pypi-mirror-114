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

"""
This example demonstrates how a node acts as the namespace which as been set as the default one
and how namespaces can be used to query channels.

Note: Namespaces have the "/" operator overloaded to easily access sub-namespaces.
When a namespace is acquired via GetNamespace() from a node, it is resolved from the root
namespace. The "/" operator allows to access namespaces relative to the nodes default namespace.

This is the assumed channel hierarchy in the above example:

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
from pulicast import ThreadedNode


def main():
    node = ThreadedNode("rover_controller", default_namespace="/drivers/rover1")

    other_ns = node.make_namespace("/flyers/glider1")

    # Access channels in default namespace and other namespace
    print(node["attitude"].name)  # drivers/rover1/attitude
    print(other_ns["attitude"].name)  # flyers/glider1/attitude

    # Access channels relative to a namespace (default or other)
    print((node / "arm")["attitude"].name)  # drivers/rover1/arm/attitude
    print((other_ns / "flap")["angle"].name)  # flyers/glider1/flap/angle
    print((other_ns / ".." / "glider2")["attitude"].name)  # flyers/glider2/attitude

    (node / "arm")["ctrl"] << "hi"


if __name__ == '__main__':
    main()