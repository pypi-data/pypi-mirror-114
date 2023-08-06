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
import trio.testing

from unittest.mock import Mock

from pulicast import TrioNode
from pulicast.pulicast_trio import open_subscription


async def test_receive_own_messages(nursery):
    node = TrioNode("test", nursery)

    logger = Mock()

    def on_msg(msg: str):
        logger(msg)

    node["test"].subscribe(on_msg)
    node["test"] << "Hi There!"

    await trio.sleep(0.1)
    logger.assert_called_once_with("Hi There!")


async def test_iterate_messages(nursery):
    node = TrioNode("test", nursery)
    channel = node["test"]

    async def publish_test_msgs():
        while True:
            channel << "Hi There!"
            await trio.sleep(.1)

    nursery.start_soon(publish_test_msgs)

    logger = Mock()
    with trio.move_on_after(1):
        async with open_subscription(channel, str) as subscription:
            async for msg in subscription:
                logger(msg)

    logger.assert_called_with("Hi There!")


async def test_subscription_handle_terminates_subscription_when_closed(nursery):
    node = TrioNode("test", nursery)
    channel = node["channelname"]

    mock = Mock()
    assert not channel.is_subscribed
    with trio.move_on_after(1):
        async with open_subscription(channel) as subscription:
            assert channel.is_subscribed
            async for msg in subscription:
                mock(msg)

    channel << "This message will trigger unsubscribing"
    await trio.sleep(0.01)  # wait a bit so that the above message can be sent and handled
    assert not channel.is_subscribed
    mock.assert_not_called()