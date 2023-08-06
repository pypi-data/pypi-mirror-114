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
from typing import Any, Optional, Callable

import trio

import pulicast
from pulicast import Channel
from pulicast.core.lead_extractor import ALL_MESSAGES_LEAD_VALUE, ORDERED_MESSAGE_LEAD_VALUE
from pulicast.node import Node
from pulicast.transport.trio_multicast_transport import TrioMulticastTransport


class TrioNode(Node):
    """
    A pulicast node that uses `Trio <https://trio.readthedocs.io/en/stable/>`_ for
    networking, timing and dispatch of subscription handlers.
    """

    def __init__(self, name: str, nursery: trio.Nursery,
                 port: int = pulicast.DEFAULT_PORT, ttl: int = 0,
                 heartbeat_period=0.1, interface_address: Optional[str] = None, default_namespace: str = "/"):
        """
        :param name: The name with which the node will be announced in the pulicast network. It is possible to announce
        multiple nodes with the same name but it is advised, that those nodes should behave in the same way (originate
        from the same executable) to avoid confusion.
        :param nursery: The nursery within all timers and subscription handlers are being started.
        :param port: The port on which to open sockets for publishing and subscribing to messages.
        :param ttl: The `time to live <https://en.wikipedia.org/wiki/Time_to_live>`_ for messages being sent.
        Set to 0 to keep the traffic on the local machine.
        :param heartbeat_period: The period in seconds with which the node should announce itself.
        :param interface_address: A network interface to bind to when sending and receiving multicast messages.
        If set to ``"0.0.0.0"`` (the default) messages will be sent and received on all network interfaces.
        Note: if you pass an invalid interface here, an exception will be thrown when making the first subscription,
        not when the node is created.
        :param default_namespace: The namespace, in which the channels are created by default.
            The default is the root namespace '/'.
        """
        self._nursery = nursery
        self._transport = TrioMulticastTransport(port, ttl, nursery, interface_address)
        super().__init__(name, default_namespace, heartbeat_period, self._transport)
        self._cancel_scope: Optional[trio.CancelScope] = None
        self.stopped = trio.Event()

        async def announce_node():
            with trio.CancelScope() as self._cancel_scope:
                while True:
                    self.announce_node()
                    await trio.sleep(heartbeat_period)
            self.stopped.set()

        self._nursery.start_soon(announce_node)

    def stop(self):
        """
        Terminates the announcement of this node. Ongoing subscriptions stay active. However, using the node after this
         is undefined.

         .. TODO(max): ensure all subscriptions are being cancelled as well.
        """
        if self._cancel_scope is not None:
            self._cancel_scope.cancel()
        self._transport.stop()

    @property
    def nursery(self):
        return self._nursery

    def run_later(self, delay: float, callback: Callable[[], None]):
        """
        Runs a function after some delay using a an async routine.

        Note: There are no accuracy guarantees for callbacks scheduled this way.

        :param delay: The time in seconds to wait before executing the callback.
        :param callback: The function to execute.
        """
        async def wait_and_call_callback():
            await trio.sleep(delay)
            callback()
        self._nursery.start_soon(wait_and_call_callback)


def open_subscription(channel: Channel, message_type: type = Any,
                      min_lead=ALL_MESSAGES_LEAD_VALUE) -> trio.MemoryReceiveChannel:
    """
    Opens a subscription, that forwards all received messages to a trio.MemoryReceiveChannel.

    Note: Do not confuse the trio.MemoryReceiveChannel with a pulicast channel! It is an entirely different concept.
    Read more about trio channels at
    https://trio.readthedocs.io/en/stable/reference-core.html#using-channels-to-pass-values-between-tasks

    The returned trio channel acts more like a file handle with async capabilities:
    1. You can wait for the next message with `msg = await subscription.read()` (returns immediately if there is a message left in the receive channel)
    2. You can asynchronously iterate the incoming messages with `async for msg in subscription: ...`
    3. You can ensure the subscription is closed after you are done with it by using it as an async context manager like
    ```python
    async with open_subscription(channel) as subscription: 
        do_something_with(subscription)
    ```

    Look at the trio_channel_iteration example for an illustration on how to use it.

    Note: When the trio.MemoryReceiveChannel is closed, the pulicast subscription is not terminated immediately.
    Unsubscribing is delayed until the next message arrives on the pulicast channel.

    :param channel: The channel to read messages from.
    :param message_type: The type of the message to expect. Use Any or None to receive all message types.
    :param min_lead: The minimum lead of the arriving messages. By default all messages are received.
    :return: A trio memory channel, that acts as a subscription handle.
    """
    send_channel, receive_channel = trio.open_memory_channel(float("inf"))

    def on_msg(msg: message_type):
        try:
            send_channel.send_nowait(msg)
        except trio.BrokenResourceError:
            subscription.unsubscribe()

    subscription = channel.subscribe(on_msg, min_lead=min_lead, with_handle=True)

    return receive_channel


def open_ordered_subscription(channel: Channel, message_type: type = Any) -> trio.MemoryReceiveChannel:
    """
    Like `messages_on` but only receives ordered messages. Unordered messages are dropped.

    :param channel: The channel to read messages from.
    :param message_type: The type of the message to expect. Use Any or None to receive all message types.
    :return: A memory channel from which the messages can be read asynchronously.
    """
    return open_subscription(channel, message_type, ORDERED_MESSAGE_LEAD_VALUE)


async def next_message_on(channel: Channel, message_type=Any, min_lead=ALL_MESSAGES_LEAD_VALUE):
    """
    Awaits the next message arriving on the given channel.

    :param channel: The channel to read messages from.
    :param message_type: The type of the message to expect. Use Any or None to receive all message types.
    :param min_lead: The minimum lead of the arriving messages. By default all messages are received.
    :return: The next arriving message on the given channel.
    """
    async with open_subscription(channel, message_type=message_type, min_lead=min_lead) as messages:
        async for msg in messages:
            return msg


async def next_ordered_message_on(channel: Channel, message_type=Any):
    """
    Like `next_message_on` but only receives ordered messages. Unordered messages are dropped.

    :param channel: The channel to read messages from.
    :param message_type: The type of the message to expect. Use Any or None to receive all message types.
    :return: The next arriving message on the given channel.
    """
    await next_message_on(channel, message_type, ORDERED_MESSAGE_LEAD_VALUE)
