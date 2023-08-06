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
import random
from typing import Callable

from pulicast_messages import pulicast_node, pulicast_channel

from pulicast.core.channel_store import ChannelStore
from pulicast.channel import Channel
from pulicast.core.transport import Transport
from pulicast.core.utils.name_resolution import resolve_name
from pulicast.namespace import Namespace


class Node(Namespace):
    """
    The node is the central handle to the pulicast API. It provides access to Channels for publishing and subscribing
    and announces itself in the pulicast network to enable global discovery of other nodes.
    The node class is an abstract class. Depending on the underlying event loop to use such as Qt, Trio or just plain
    sockets with threads there are subclasses, that set up the node with the corresponding event loop mechanism.

    Notes for subclassing Node:
    The node class does not start the periodic announcement of the node in the pulicast network. For this, subclasses
    must  call the :func:`announce_node` function in regular intervals according to the given announcement period.

    .. TODO(max): since there is the run_later function now Node could actually implement this itself. The run_later function must be implemented by subclasses.

    .. TODO(max): This mix of having to override a function and passing multicast transport to the constructor is ugly design.
    """

    def __init__(self, name: str, default_namespace: str, heartbeat_period: float, transport: Transport):
        """
        Creates a new pulicast node operating with the given multicast sender and multicast receiver.

        :param name: The name with which the node will be announced in the pulicast network. It is possible to announce
        multiple nodes with the same name but it is advised, that those nodes should behave in the same way (originate
        from the same executable) to avoid confusion.
        :param default_namespace: The namespace, in which the channels are created by default.
            The default should be the root namespace '/'.
        :param heartbeat_period: The period in seconds with which the node should announce itself.
        :param transport: The Transport to be used for sending and receiving messages.
         groups.
        """
        self._channel_store = ChannelStore(transport)
        super().__init__(self._channel_store, default_namespace)
        self._node_info = pulicast_node()
        self._node_info.name = name
        self._node_info.session_id = random.randint(-(1 << 63), (1 << 63) - 1)

        self._nodes_channel = self._channel_store["__nodes"]
        self._nodes_channel.publishing_period = heartbeat_period

        # This is to announce the node immediately when the channels changed.
        # Otherwise this would be delayed until the next regular announcement of the node.
        # TODO: for some reason it is important, that this callback is registered AFTER the __nodes channel
        #  has been created. But I forgot why. We should find this out and document it.
        self._channel_store.add_on_item_added_callback(lambda c: self.announce_node(), False)

    def announce_node(self):
        """
        Announces the node within the pulicast network by sending a heartbeat message with its name and session id
        to the `__nodes` channel.

        See the section about Node Liveness Detection for details.

        .. TODO(max): reference this
        """
        # TODO(max): for simplicity we send entire node_info objects as a heartbeat.
        #  An optimization would be to just send se session ID, name and hash of channel infos as a heartbeat.
        #  The node information should only be delivered upon request. An interested node observer can then just request
        #  The list of nodes whenever the hash of channel infos changes.
        self._node_info.channels = [self._make_channel_info(channel) for channel in self._channel_store]
        self._node_info.num_channels = len(self._node_info.channels)
        self._nodes_channel << self._node_info

    def make_namespace(self, namespace: str) -> Namespace:
        return Namespace(self._channel_store, namespace)

    @property
    def heartbeat_period(self):
        """The period in seconds between two node announcements."""
        return self._nodes_channel.publishing_period

    @property
    def session_id(self):
        """The unique id of the node."""
        return self._node_info.session_id

    @property
    def name(self):
        return self._node_info.name

    @staticmethod
    def _make_channel_info(channel: Channel):
        """Constructs a pulicast_messages.pulicast_channel message based on the channels that are currently in use byt
        this node."""
        channel_info = pulicast_channel()
        channel_info.name = channel.name
        channel_info.publishing_period_ns = int(channel.publishing_period * 1e9)
        channel_info.is_published = channel.is_published
        channel_info.is_subscribed = channel.is_subscribed
        return channel_info

    def run_later(self, delay: float, callback: Callable[[], None]):
        """
        Runs a function after some delay using the underlying event loop.

        Note: There are no accuracy guarantees for callbacks scheduled this way.

        Note: This is an abstract method to be implemented by subclasses of Node.

        :param delay: The time in seconds to wait before executing the callback.
        :param callback: The function to execute.
        """
        raise NotImplementedError()

    def __iter__(self):
        return self._channel_store.__iter__()

    def __next__(self):
        return self._channel_store.__iter__()