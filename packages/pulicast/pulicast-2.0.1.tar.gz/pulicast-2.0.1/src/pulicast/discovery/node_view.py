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
import time

from pulicast_messages import pulicast_node, pulicast_channel

from pulicast.core.utils.observable_dict import ObservableDict
from pulicast.core.utils.observable_set import ObservableSet
from pulicast.address import Address


class Publication:
    """Describes that a node publishes on a channel with a given period."""
    __slots__ = "name", "period"

    def __init__(self, name: str, period: float):
        self.name = name
        self.period = period


class NodeView:
    """The :class:`.NodeView` class describes a remote node with its name, session id and channels."""

    def __init__(self, node_info: pulicast_node, source: Address):
        super().__init__()
        self._name = node_info.name
        self._session_id = node_info.session_id
        self._source = source

        self._subscriptions: ObservableSet[str] = ObservableSet(
            info.name for info in node_info.channels if info.is_subscribed)
        self._publications: ObservableDict[str, Publication] = ObservableDict(
            {info.name: Publication(info.name, info.publishing_period_ns / 1e9) for info in node_info.channels if
             info.is_published})
        self._channels: ObservableSet[str] = ObservableSet(info.name for info in node_info.channels)

        self._heartbeat_period: int = \
            [info.publishing_period_ns / 1e9 for info in node_info.channels if info.name == "__nodes"][0]
        self._deadline = time.time() + self.heartbeat_period * 3

    @property
    def is_dead(self) -> bool:
        """Checks if the last heartbeat of the node is longer away than its heartbeat period allows."""
        return time.time() > self._deadline

    @property
    def deadline(self) -> float:
        """The time after which the node is considered dead unless another heartbeat arrives."""
        return self._deadline

    @property
    def heartbeat_period(self):
        """The expected interval between two heartbeats."""
        return self._heartbeat_period

    def update(self, node_info: pulicast_node, source: Address):
        """
        Update the node views deadline and channels with a heartbeat message of type
        :class:`pulicast_messages.pulicast_node`.

        Usually this would be called by the node discoverer whenever a new heartbeat message arrives.
        User code should only call this for testing purposes.
        """
        self._ensure_invariant_info_matches(node_info, source)
        self._update_channels(node_info)
        self._advance_deadline()

    @property
    def subscriptions(self) -> ObservableSet[str]:
        """Observable set of the channels that the node subscribes to."""
        return self._subscriptions

    @property
    def publications(self) -> ObservableDict[str, Publication]:
        """An observable map containing :class:`.Publication` information for all channels the node publishes to"""
        return self._publications

    @property
    def channels(self) -> ObservableSet[str]:
        """
        An observable set  of channels that the node uses.

        .. note::
            This is not necessarily the union of subscribed and published channels since it is possible for a node to
            announce that it is using a channel without subscribing it or publishing on it.
        """
        return self._channels

    @property
    def name(self):
        return self._name

    @property
    def session_id(self):
        return self._session_id

    @property
    def source(self):
        return self._source

    def _ensure_invariant_info_matches(self, node_info: pulicast_node, source: Address):
        # TODO(max): also check if the publishing period changed
        if self.name != node_info.name:
            raise RuntimeWarning(
                f"The node with session ID {node_info.session_id} previously known as {self.name} "
                f"now announces itself as {node_info.name}!"
                f"This is strange and coule mean "
                f"1. the node altered its name while running "
                f"2. an old node under this name died and a new one started with the same (random) session ID")
        if self.session_id != node_info.session_id:
            raise RuntimeWarning(
                f"The session {self.session_id} changed its session id to {node_info.session_id}!"
                f"This should actually be impossible with the current implementation!"
            )  # TODO(max): more detailed message here. Ref issue #11
        if self.source != source:
            raise RuntimeWarning(
                f"The node {self.name} with id {self.session_id} changed the source address it is publishing from!"
                f"Previously it published from {self.source} but now a message came from {source}."
                f"This is highly suspicious and looks like somebody hijacked the identity of another node!"
                f"You should immediately investigate this and stop trusting anybody in your network.")

    def _update_channels(self, node_info: pulicast_node):
        # NOTE: we don't care for removed channels because we do not support unsubscribing yet
        for channel_info in node_info.channels:
            channel_info: pulicast_channel
            if channel_info.is_published:
                # NOTE: here we could check that the new publishing period corresponds to the already stored publishing
                #  period and ensure that they are equal to detect faulty implementations. But we don't
                self.publications[channel_info.name] = Publication(channel_info.name,
                                                                   channel_info.publishing_period_ns / 1e9)

            if channel_info.is_subscribed:
                self.subscriptions.add(channel_info.name)

            self.channels.add(channel_info.name)

    def _advance_deadline(self):
        self._deadline = time.time() + self.heartbeat_period * 3
