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

from pulicast import TrioNode
from pulicast.pulicast_trio import next_message_on, open_subscription


async def main():
    async with trio.open_nursery() as nursery:
        node = TrioNode("iterator", nursery)

        nursery.start_soon(node.announce_node_forever)

        the_next_best_announcement = await next_message_on(node["/__nodes"])
        print(the_next_best_announcement)

        # by using the node_messages as a manager, we ensure that the subscription is closed when we are done receiving
        # messages.
        async with open_subscription(node["/__nodes"]) as subscription:
            async for msg in subscription:
                print(msg)


if __name__ == '__main__':
    trio.run(main)
