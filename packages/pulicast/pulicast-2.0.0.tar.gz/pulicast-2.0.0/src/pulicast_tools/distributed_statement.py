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
>>> is_is_statement_channel("asd")
"""

import math
from typing import Any, Optional

import trio
from trio import Nursery

from pulicast import Channel, Node
from pulicast.core.utils.observable_dict import ObservableDict
from pulicast.discovery.node_view import NodeView, Publication
from pulicast.namespace import Namespace
from pulicast.pulicast_trio import open_subscription
from pulicast_tools.puliconf.setting_view import zcm_msg_equals




def is_statement_channel(channel_name: str):
    return ".statements/" in channel_name and not channel_name.endswith(".rev") and not channel_name.endswith(".req")


def is_revision_channel(channel_name: str):
    return channel_name.endswith(".statements/.rev")


def is_request_channel(channel_name: str):
    return channel_name.endswith(".statements/.req")


class StatementGroup:
    def __init__(self, node: Node, nursery: Nursery, announce_period: float = 0.1):
        self._revision_channel = (node / ".statements")[".rev"]
        self._current_revision = 0
        self._namespace = node

        async def periodically_publish_revision():
            while True:
                self._revision_channel << self._current_revision
                await trio.sleep(announce_period)

        nursery.start_soon(periodically_publish_revision)

    def increase_revision(self):
        self._current_revision += 1
        self._revision_channel << self._current_revision

    @property
    def namespace(self) -> Namespace:
        return self._namespace

    def make_statement(self, name: str, value: Optional[Any] = None):
        statement = DistributedStatement(name, self)
        if value is not None:
            statement.value = value
        return statement


class DistributedStatement:

    def __init__(self, name: str, statement_group: StatementGroup):
        self._value = None
        namespace = statement_group.namespace
        self._announce_channel = (namespace / ".statements")[name]
        self._req_channel = (namespace / ".statements")[".req"]
        self._statement_group = statement_group

        self._req_channel.subscribe(lambda : self._announce_channel << self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not zcm_msg_equals(self.value, new_value):
            self._value = new_value
            self._announce_channel << self._value
            self._statement_group.increase_revision()

    @property
    def name(self) -> str:
        return deduce_name_from_statement_channel(self._announce_channel.name)

class RevisionView:
    def __init__(self, revision_channel: Channel):
        assert is_revision_channel(revision_channel.name)
        self._last_revision_update_timestamp = -math.inf
        self._last_revision_pulse_timestamp = -math.inf
        self._last_known_revision = -math.inf
        self._next_revision_event = trio.Event()

        def update_revision(new_revision: int):
            self._last_revision_pulse_timestamp = trio.current_time()
            if self._last_known_revision != new_revision:
                self._last_revision_update_timestamp = trio.current_time()
                self._last_known_revision = new_revision
                self._next_revision_event.set()
                self._next_revision_event = trio.Event()

        revision_channel.subscribe(update_revision)

    @property
    def revision_age(self) -> float:
        return trio.current_time() - self._last_revision_update_timestamp

    @property
    def view_age(self) -> float:
        return trio.current_time() - self._last_revision_pulse_timestamp

    @property
    def revision(self) -> int:
        return self._last_known_revision

    async def wait_next_revision(self):
        await self._next_revision_event
        return self.revision


class StatementView:
    def __init__(self, channel: Channel, req_channel: Channel):
        self._last_update_timestamp = -math.inf


        self._last_value = None
        self._channel = channel
        self._req_channel = req_channel

        self._updated = trio.Event()

        def update_value(new_value: Any):
            self._last_value = new_value
            self._last_update_timestamp = trio.current_time()
            self._updated.set()
            self._updated = trio.Event()

        channel.subscribe(update_value)



    @property
    def age(self) -> float:
        return trio.current_time() - self._last_update_timestamp

    @property
    def value(self):
        return self._last_value

    @property
    def name(self) -> str:
        return deduce_name_from_statement_channel(self._channel.name)

    async def next_value(self):
        await self._updated.wait()
        return self.value

    async def request_value(self):
        async with open_subscription(self._channel) as sub:
            self._req_channel << "where dada?"
            async for value in sub:
                return value

    async def _ensure_age(self):
        pass



def deduce_name_from_statement_channel(channel_name: str):
    assert is_statement_channel(channel_name), f"{channel_name} must be a statement channel!"
    return channel_name.split("/")[-1]


class StatementGroupView(ObservableDict[str, StatementView]):

    def __init__(self, node_view: NodeView, namespace: Namespace):
        ObservableDict.__init__(self)
        self._revision_channel = (namespace / ".statements")[".rev"]
        self._req_channel = (namespace / ".statements")[".req"]
        self._req_channel << "where data?"

        self._last_known_revision = -math.inf

        def set_newest_revision(revision: int):
            if revision != self._last_known_revision:
                # TODO: update all the views
                self._last_known_revision = revision

        self._revision_channel.subscribe(set_newest_revision)

        def setup_new_view_if_is_statement_announce_channel(pub: Publication):
            if pub.name.startswith(str(namespace)) and is_statement_channel(pub.name):
                view = StatementView((namespace / ".statements")[deduce_name_from_statement_channel(pub.name)], self._req_channel)
                self[view.name] = view

        node_view.publications.add_on_item_added_callback(setup_new_view_if_is_statement_announce_channel)