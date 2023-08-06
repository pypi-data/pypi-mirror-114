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
import logging
from typing import Callable, Generator, Optional

import trio

from pulicast import Node
from pulicast.core.utils.observable_dict import ObservableDict
from pulicast.core.utils.observable_set import ObservableSet
from pulicast.discovery.node_discoverer import NodeDiscoverer
from pulicast.discovery.node_view import NodeView
from pulicast.pulicast_trio import open_subscription
from pulicast_messages import poke_setting, roc_ack
from pulicast_tools.puliconf.channel_naming_conventions import deduce_confirmation_channel_from_roc_channel, \
    is_setting_roc_channel
from pulicast_tools.puliconf.setting_view import SettingView


def warn_about_conflicting_settings(old_setting: SettingView, new_setting: SettingView):
    logging.warning(f"{old_setting.owning_node.name} and {new_setting.owning_node.name} both advertise "
                    f"the setting '{old_setting.name}'! Those settings will be locked to prevent undefined behaviour!")


async def init_setting(node: Node, owning_node: NodeView, roc_channel_name: str, num_retries: int = 10,
                       retry_period: float = 0.2) -> Optional[SettingView]:
    """
    Initializes a setting that is owned by a given node by poking it until there is a confirmation and the owning node
    claims to publish on the confirmation channel.

    :param node: The node to use for publishing and subscribing.
    :param owning_node: A view of the node that is supposedly owning the setting.
    :param roc_channel_name: The name of the request of change channel used by the setting.
    :param num_retries: How often to poke until giving up.
    :param retry_period: How long to wait between pokes in seconds.
    :return: An initialized SettingView or None when there was no answer or the owning node never claimed to have sent
     it.
    """
    roc_channel = node["/" + roc_channel_name]
    setting_channel = node["/" + deduce_confirmation_channel_from_roc_channel(roc_channel_name)]

    async with open_subscription(setting_channel, message_type=roc_ack, min_lead=1) as conf_messages:
        next_poke_time = trio.current_time()
        for _ in range(num_retries):
            roc_channel << poke_setting()

            next_poke_time += retry_period

            with trio.move_on_at(next_poke_time):
                confirmation = await conf_messages.receive()
                if setting_channel.name in owning_node.publications:
                    return SettingView(setting_channel.name, confirmation, owning_node, node)
                else:
                    # Note: this ensures that we do not send pokes too fast in case of faulty confirmations
                    await trio.sleep_until(next_poke_time)
    return None


class SettingDiscoverer(ObservableDict[NodeView, ObservableDict[str, SettingView]]):
    """
    The settings discoverer finds nodes in the pulicast network, that advertise a distributed setting and maintains
    a collection of :class:`.SettingView`s onto those distributed settings.
    It is an :class:`.ObservableDict`, that maps :class:`.NodeView`s to observable dicts of :class:`.SettingView`s.
    If you need a flat view on the settings, use a :class:`.SettingsSet`, which can be acquired from the setting
    discoverers `settings_set` property.
    """

    def __init__(self, node: Node, nursery: trio.Nursery, node_discoverer: NodeDiscoverer):
        """
        Creates a new SettingDiscoverer.

        :param node: The pulicast node to use to access the pulicast network.
        :param nursery: A trio nursery to schedule settings initialization tasks to.
        :param node_discoverer: A node discoverer, to discover new nodes, that potentially advertise settings.
        """
        super().__init__()

        self._node = node
        self._nursery = nursery

        node_discoverer.add_on_item_added_callback(self._ensure_setting_views_for_node_are_initialized)
        node_discoverer.add_on_item_removed_callback(self._lock_nodes_settings_and_remove_node_entry)

        self._settings_set = SettingsSet(self)

    @property
    def settings_set(self) -> 'SettingsSet':
        """
        :return: Get a flaw view on the discovered settings as a :class:`.SettingsSet`.
        """
        return self._settings_set

    def _ensure_setting_views_for_node_are_initialized(self, node: NodeView):
        async def init_and_add_setting(roc_channel: str):
            setting = await init_setting(self._node, node, roc_channel)
            if setting is not None:
                self._add_setting(node, setting)
            elif "__nodes" not in node.subscriptions:
                logging.warning(f"{node.name} subscribes to {roc_channel} but does not answer pokes or does not advertise its publishement"
                                f" corresponding distributed setting!")
            else:
                pass

        def init_setting_if_is_roc_channel(channel: str):
            if is_setting_roc_channel(channel) and "__nodes" not in node.subscriptions:
                self._nursery.start_soon(init_and_add_setting, channel)

        node.subscriptions.add_on_item_added_callback(init_setting_if_is_roc_channel)

    def _lock_nodes_settings_and_remove_node_entry(self, node: NodeView):
        if node in self:
            for setting in self[node]:
                # Note: we need to make sure that those disappeared settings are locked to prevent that they are
                # accidentally used.
                setting.lock()
            # Note: We explicitly clear the dict of SettingViews to notify potential listeners to that event
            self[node].clear()
            del self[node]

    def _add_setting(self, owning_node: NodeView, setting: SettingView):
        if owning_node not in self:
            self[owning_node] = ObservableDict()
        self[owning_node][setting.name] = setting


class SettingsSet(ObservableSet[SettingView]):
    """
    A settings set represents the set of all settings that were found by a given :class:`.SettingDiscoverer`.
    It will ensure that duplicate settings are locked and it allows to register a callback for the case that there is
    a duplicate setting.
    """
    def __init__(self, setting_discoverer: SettingDiscoverer):
        super().__init__()

        self.duplicate_setting_callback: Optional[Callable[[SettingView, SettingView], None]] = \
            warn_about_conflicting_settings
        setting_discoverer.add_on_item_added_callback(self._on_new_node_with_settings_appeared)

    def _on_new_node_with_settings_appeared(self, settings_dict: ObservableDict[str, SettingView]):

        def on_setting_added(new_setting: SettingView):
            self._lock_duplicate_settings(new_setting)
            self._call_duplicate_setting_callback(new_setting)
            self.add(new_setting)

        settings_dict.add_on_item_added_callback(on_setting_added)
        settings_dict.add_on_item_removed_callback(self.remove)

    def _lock_duplicate_settings(self, new_setting: SettingView):
        for colliding_setting in self.settings_with_name(new_setting.name):
            new_setting.lock()
            colliding_setting.lock()

    def _call_duplicate_setting_callback(self, new_setting: SettingView):
        if self.duplicate_setting_callback is not None:
            for colliding_setting in self.settings_with_name(new_setting.name):
                self.duplicate_setting_callback(colliding_setting, new_setting)

    def settings_with_name(self, name: str) -> Generator[SettingView, None, None]:
        return (s for s in self if s.name == name)
