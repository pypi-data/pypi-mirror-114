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
import importlib
import logging
import math
import warnings
from typing import Any, Iterable, List, Optional, Type

import tomlkit
import trio
from tomlkit.toml_document import TOMLDocument

from pulicast.core.utils.observable_container import ObservableContainer, T
from pulicast_tools.puliconf.setting_discoverer import SettingsSet
from pulicast_tools.puliconf.setting_view import SettingView, zcm_msg_equals


async def pull_configuration(settings_set: SettingsSet) -> TOMLDocument:
    await wait_until_no_new_setting_appeared(settings_set)
    return convert_settings_to_toml(settings_set)


async def push_configuration(settings_set: SettingsSet, toml_doc: TOMLDocument, reset_first=False, unset_first=False):
    await wait_until_no_new_setting_appeared(settings_set)
    return await apply_toml_to_settings(toml_doc, settings_set, reset_first, unset_first)


async def diff_configuration(settings_set: SettingsSet, toml_doc: TOMLDocument):
    await wait_until_no_new_setting_appeared(settings_set)

    settings_by_name = {s.name: s for s in settings_set}

    diff_doc = TOMLDocument()
    for setting_name, target_value in toml_doc.items():
        if setting_name not in settings_by_name:
            logging.error(f"Could not set {setting_name} to {target_value} since the setting is not owned by any node!")
            continue
        setting = settings_by_name[setting_name]

        serializable_target_value = convert_toml_value_to_puli_serializable(target_value, setting.value_type)
        if not zcm_msg_equals(serializable_target_value, setting.value):
            diff_doc.append(setting_name, target_value)

    return diff_doc


async def wait_until_no_new_setting_appeared(settings_set: SettingsSet, duration: float = 2):
    """Waits until no new settings appeared in the given settings set for the given duration"""
    with trio.move_on_after(duration) as cancel_scope:
        async with items_in_observable_container(settings_set) as new_settings:
            async for _ in new_settings:
                cancel_scope.deadline = trio.current_time() + duration


def items_in_observable_container(container: ObservableContainer[T]) -> trio.MemoryReceiveChannel:
    """Opens a trio.MemoryReceiveChannel on which all new items in an observable container will appear."""
    send_channel, receive_channel = trio.open_memory_channel(math.inf)

    def put_new_item_on_channel(item: T):
        try:
            send_channel.send_nowait(item)
        except trio.BrokenResourceError:
            container.remove_on_item_added_callback(put_new_item_on_channel)

    container.add_on_item_added_callback(put_new_item_on_channel)

    return receive_channel


def convert_puli_serializable_to_toml_value(value):

    if hasattr(value, "__slots__"):
        d = dict()
        d["__msg_type__"] = type(value).__module__
        for field in value.__slots__:
            field_value = getattr(value, field)
            d[field] = convert_puli_serializable_to_toml_value(field_value)
        return d
    elif isinstance(value, (list, tuple)):
        return [convert_puli_serializable_to_toml_value(i) for i in value]
    else:
        # Note: we encode None as NaN since TOML does not support None values
        return float("nan") if value is None else value


def convert_toml_value_to_puli_serializable(d: Any, expected_value_type: Optional[Type] = None):
    if isinstance(d, dict) and "__msg_type__" in d:
        # Note: here we create a new object of the type specified in the field __msg_type__
        module = d['__msg_type__']
        msg = getattr(importlib.import_module(module), module.split(".")[-1])()
        for field in filter(lambda k: k != "__msg_type__", d.keys()):
            setattr(msg, field, convert_toml_value_to_puli_serializable(d[field]))
        msg.encode()  # check if we can encode the message to check if we unpacked correctly
        return msg
    elif isinstance(d, (list, tuple)):
        return tuple(convert_toml_value_to_puli_serializable(i) for i in d)
    elif d != d:
        return None # Note: NaN check. We encode 'None' as NaN in TOML since TOML does not support None
    elif expected_value_type is not None:
        return expected_value_type(d)
    else:
        return d


def convert_settings_to_toml(settings: Iterable[SettingView]) -> TOMLDocument:
    toml_doc = tomlkit.document()
    for setting in settings:
        # setting: SettingView = setting
        if setting.is_locked:
            continue
        if not setting.is_synced:
            warnings.warn(f"Not converting {setting} to TOML since it is not synced right now!")
            continue
        value = convert_puli_serializable_to_toml_value(setting.value)
        if value is None:  # Note: We encode 'None' as NaN in TOML since TOML does not support None
            value = float("nan")
        toml_doc[setting.name] = value
        if setting.initialization_message != "":
            toml_doc[setting.name].comment(setting.initialization_message)

    return toml_doc


async def apply_toml_to_settings(toml_doc: TOMLDocument, settings: SettingsSet, reset_first=False, unset_first=False):
    settings_by_name = {s.name: s for s in settings}

    changed_settings: List[SettingView] = []
    failed_settings: List[SettingView] = []
    unchanged_settings: List[SettingView] = []
    for setting_name, target_value in toml_doc.items():
        if setting_name not in settings_by_name:
            logging.error(f"Could not set {setting_name} to {target_value} since the setting is not owned by any node!")
            continue
        setting = settings_by_name[setting_name]

        if reset_first:
            success, warning = await setting.reset()
            if not success:
                logging.error(f"Could not reset {setting}: {warning}")
                unchanged_settings.append(setting)
                continue

        if unset_first:
            success, warning = await setting.unset()
            if not success:
                logging.error(f"Could not unset {setting}: {warning}")
                unchanged_settings.append(setting)
                continue

        target_value = convert_toml_value_to_puli_serializable(target_value, setting.value_type)
        if not zcm_msg_equals(target_value, setting.value):
            success, warning = await setting.set(target_value)
            if success:
                changed_settings.append(setting)
            if not success:
                logging.error(f"Could not set {setting}: {warning}")
                failed_settings.append(setting)
        else:
            unchanged_settings.append(setting)
    return changed_settings, unchanged_settings, failed_settings

