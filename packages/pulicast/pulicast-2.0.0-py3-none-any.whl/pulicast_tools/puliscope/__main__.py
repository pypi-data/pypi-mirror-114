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
import argparse

import qtrio
import trio

import pulicast
from pulicast.pulicast_qt import QtNode
from pulicast_tools.puliscope.main_window import MainWindow


async def async_main():
    parser = argparse.ArgumentParser(description="A tool to display active pulicast nodes and their channels.")
    parser.add_argument("-p", "--port", type=int, default=pulicast.DEFAULT_PORT, help="The pulicast port to listen on.")
    args = parser.parse_args()

    node = QtNode("puliscope", port=args.port)

    try:
        async with trio.open_nursery() as nursery:
            main_window = MainWindow(node, nursery)
            main_window.show()

            main_window_closed = trio.Event()
            main_window.closed.connect(main_window_closed.set)
            await main_window_closed.wait()
    except KeyboardInterrupt:
        pass


def main():
    qtrio.run(async_main)


if __name__ == '__main__':
    main()