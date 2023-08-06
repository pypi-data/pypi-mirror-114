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
import pulicast_messages
from tests.utils.mock_node import make_mock_node
from tests.utils.mock_subscriptions import setup_mock_subscription, assert_called_once_with_message, \
    last_received_message


def test_announce_node():
    """Ensure that a proper announcement package is sent out when a node announces itself."""
    # GIVEN
    node = make_mock_node()

    # WHEN
    # Publish some data on some channels to make it more interesting
    for i in range(10):
        node[f"channel_{i}"] << "Some Data"

    # Subscribe to the __nodes channel where nodes are announced
    nodes_subscription = setup_mock_subscription(pulicast_messages.pulicast_node, None, None, False, node["__nodes"], False)

    # Actually announce the node
    node.announce_node()

    # THEN
    assert_called_once_with_message(nodes_subscription, node.name, "name")
    assert_called_once_with_message(nodes_subscription, node.session_id, "session_id")
    assert_called_once_with_message(nodes_subscription, len(node._channel_store), "num_channels")

    announced_channels = {channel.name for channel in last_received_message((nodes_subscription)).channels}
    actual_channels = {channel.name for channel in node._channel_store}
    assert announced_channels == actual_channels


def test_initialization():
    # GIVEN
    node = make_mock_node()

    # THEN
    assert type(node.session_id) == int
    assert node.name == "mock_node"
    assert node.heartbeat_period == 0.1


def test_session_id_collisions():
    """
    Test that for a large number of nodes there will be no session id collision. This is just a heuristic of course.
    """
    # GIVEN
    node1 = make_mock_node()

    # THEN
    for _ in range(100000):
        node2 = make_mock_node()
        assert node1.session_id != node2.session_id