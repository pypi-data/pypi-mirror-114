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
import copy
from typing import Tuple

import pytest
import trio

from pulicast import Node, TrioNode
from pulicast.discovery.node_discoverer import NodeDiscoverer
from pulicast_messages import pulicast_channel, pulicast_node
from pulicast_tools.puliconf.setting import Setting
from pulicast_tools.puliconf.setting_discoverer import SettingDiscoverer
from pulicast_tools.puliconf.setting_view import SettingView, zcm_msg_equals


test_channel_msg = pulicast_channel()
test_channel_msg.name = "Test"
test_channel_msg.is_subscribed = True
test_channel_msg.is_published = False
test_channel_msg.publishing_period_ns = 555

test_node_msg = pulicast_node()
test_node_msg.name = "asd"
test_node_msg.channels = [test_channel_msg]
test_node_msg.num_channels = 1


@pytest.mark.parametrize("msg", [0, 0., 1, 1. - 1, "Test", test_channel_msg, test_node_msg])
def test_zcm_msg_equals_identity(msg):
    assert zcm_msg_equals(msg, msg)
    assert zcm_msg_equals(msg, copy.copy(msg))
    assert zcm_msg_equals(msg, copy.deepcopy(msg))


def test_zcm_does_not_equal():
    assert not zcm_msg_equals(1, 2)
    assert not zcm_msg_equals(1, 2.)
    assert not zcm_msg_equals(1, "asd")
    assert not zcm_msg_equals("asdf", "asd")
    assert not zcm_msg_equals(test_channel_msg, test_node_msg)
    assert not zcm_msg_equals(test_node_msg, 5)


@pytest.fixture(params=[float(0.1), int(-1), str("test"), test_node_msg, test_channel_msg])
async def node_and_setting(nursery, request) -> Tuple[Node, Setting]:
    node = TrioNode("owning_node", nursery)
    return node, Setting("test_setting", node, request.param)


@pytest.fixture
async def node_and_node_discoverer(nursery) -> Tuple[Node, NodeDiscoverer]:
    node = TrioNode("discovering_node", nursery)
    return node, NodeDiscoverer(node)


@pytest.fixture
async def node_and_setting_discoverer(node_and_node_discoverer) -> Tuple[Node, SettingDiscoverer]:
    node, discoverer = node_and_node_discoverer
    return node, SettingDiscoverer(node, node.nursery, discoverer)


@pytest.fixture
async def setting_and_settingview(node_and_setting, node_and_setting_discoverer) \
        -> Tuple[Tuple[Node, Setting], Tuple[Node, SettingView]]:
    """
    Sets up a node owning a setting and another node discovering that setting using a setting discoverer.
    After the setting has been discovered, the the setting and its view are returned together with their respective
    nodes.
    """
    discovering_node, discoverer = node_and_setting_discoverer
    owning_node, setting = node_and_setting

    setting_view_holder = []
    setting_discovered = trio.Event()

    def store_view_and_notify_if_matching_setting(setting_view: SettingView):
        if setting_view.owning_node.name == owning_node.name and setting.name == setting_view.name:
            setting_view_holder.append(setting_view)
            setting_discovered.set()

    discoverer.settings_set.add_on_item_added_callback(store_view_and_notify_if_matching_setting)

    await setting_discovered.wait()
    return node_and_setting, (discovering_node, setting_view_holder[0])


def assert_setting_equals_view(setting: Setting, view: SettingView):
    assert view is not None
    assert view.is_synced
    assert not view.is_locked
    assert view.name == setting.name
    assert zcm_msg_equals(view.value, view.value)


async def test_setting_discovery(setting_and_settingview):
    # GIVEN
    (owning_node, setting), (discovering_node, setting_view) = setting_and_settingview

    # THEN
    assert_setting_equals_view(setting, setting_view)


async def test_set_setting(setting_and_settingview):
    # GIVEN
    (owning_node, setting), (discovering_node, setting_view) = setting_and_settingview
    target_value = make_modified_version(setting.value)

    # WHEN
    success, warning = await setting_view.set(target_value)

    # THEN
    assert success, warning
    assert zcm_msg_equals(setting.value, target_value)
    assert_setting_equals_view(setting, setting_view)


async def test_set_setting_to_wrong_value(setting_and_settingview):
    # GIVEN
    (owning_node, setting), (discovering_node, setting_view) = setting_and_settingview
    wrong_value = list()

    # WHEN
    success, warning = await setting_view.set(wrong_value)

    # THEN
    assert not success, warning
    assert "Can only set" in warning and " to values of type" in warning and "and not of type" in warning
    assert_setting_equals_view(setting, setting_view)


async def test_unset_setting(setting_and_settingview):
    # GIVEN
    (owning_node, setting), (discovering_node, setting_view) = setting_and_settingview

    # WHEN
    success, warning = await setting_view.unset()

    # THEN
    assert success, warning
    assert setting.value is None
    assert setting_view.value is None
    assert_setting_equals_view(setting, setting_view)


async def test_reset_setting(setting_and_settingview):
    # GIVEN
    (owning_node, setting), (discovering_node, setting_view) = setting_and_settingview
    initial_value = setting.value
    intermediate_value = make_modified_version(setting.value)

    # WHEN
    success, warning = await setting_view.set(intermediate_value)

    # THEN
    assert success, warning
    assert zcm_msg_equals(setting.value, intermediate_value)

    # WHEN
    success, warning = await setting_view.reset()

    # THEN
    assert success, warning
    assert zcm_msg_equals(setting.value, initial_value)


def make_modified_version(value):
    """Generates a value of the same type as the given value but with a different value."""
    if isinstance(value, pulicast_node):
        modified_value = pulicast_node()
        modified_value.name = "xyz"
    elif isinstance(value, pulicast_channel):
        modified_value = pulicast_channel()
        modified_value.name = "xyz"
    else:
        modified_value = value * 2

    return modified_value

