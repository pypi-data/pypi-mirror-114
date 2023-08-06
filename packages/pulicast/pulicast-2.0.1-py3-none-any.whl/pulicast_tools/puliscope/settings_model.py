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
import typing
from typing import Dict

from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QColor, QStandardItem, QStandardItemModel
from trio import Nursery

from pulicast import Node
from pulicast_tools.puliconf.setting_discoverer import SettingDiscoverer
from pulicast_tools.puliconf.setting_view import SettingView


class SettingNameItem(QStandardItem):
    def __init__(self, setting: SettingView):
        QStandardItem.__init__(self, setting.name)
        self.setEditable(False)
        self.setSelectable(False)

        default_background = self.background()
        red_background = QBrush(QColor("red"))

        def set_red_background_if_not_synced(is_synced: bool):
            self.setBackground(default_background if is_synced else red_background)

        set_red_background_if_not_synced(setting.is_synced)

        SettingView.is_synced.add_on_changed_callback(setting, set_red_background_if_not_synced)


class SettingValueItem(QStandardItem):
    def __init__(self, setting: SettingView, nursery: Nursery):
        self._setting = setting
        self._nursery = nursery
        QStandardItem.__init__(self, str(setting.value))
        self.setEditable(True)
        self.setCheckable(False)

        def disable_if_locked(is_locked: bool):
            self.setEnabled(not is_locked)

        disable_if_locked(setting.is_locked)
        SettingView.is_locked.add_on_changed_callback(setting, disable_if_locked)

    def data(self, role: int = ...) -> typing.Any:
        if role in (Qt.EditRole, Qt.DisplayRole):
            return self._setting.value
        else:
            return super().data(role)

    def setData(self, value: typing.Any, role: int = ...) -> None:
        if role == Qt.EditRole:
            self._nursery.start_soon(self.try_set_data, value)
        else:
            super().setData(value, role)

    async def try_set_data(self, value):
        success, message = await self._setting.set(value)
        self.emitDataChanged()
        if message != "":
            print(self._setting.name, message)


class SettingsModel(QStandardItemModel):
    """
    A settings model holds one row per discovered setting.
    Non-synced setting views are marked red and locked settings are disabled.
    """
    def __init__(self, node: Node, nursery: Nursery, settings_discoverer: SettingDiscoverer):
        super().__init__(0, 2)
        self.setHorizontalHeaderLabels(["Name", "Value"])

        self._node = node
        self._nursery = nursery
        self._discoverer = settings_discoverer
        self._discoverer.settings_set.add_on_item_added_callback(self._on_new_setting)
        self._discoverer.settings_set.add_on_item_removed_callback(self._on_setting_gone)

        self._setting_items_by_view: Dict[SettingView, QStandardItem] = dict()

    def _on_new_setting(self, setting: SettingView):
        setting_name_item = SettingNameItem(setting)
        setting_value_item = SettingValueItem(setting, self._nursery)
        self._setting_items_by_view[setting] = setting_name_item
        self.appendRow((setting_name_item, setting_value_item))

    def _on_setting_gone(self, setting: SettingView):
        self.removeRow(self._setting_items_by_view[setting].row())
        del self._setting_items_by_view[setting]
