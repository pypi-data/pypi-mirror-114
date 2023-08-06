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

import trio

from pulicast import TrioNode, Address


async def main():

    async with trio.open_nursery() as nursery:
        node = TrioNode("chatter", nursery)

        def msg_handler(msg: str, source: Address, lead: int):
            print(f"{source.port}: {msg}\t{lead}")

        node["channel_1"].subscribe(msg_handler)

        while True:
            node['channel_1'] << await trio.to_thread.run_sync(input, "Input Message: ")

if __name__ == '__main__':
    trio.run(main)


