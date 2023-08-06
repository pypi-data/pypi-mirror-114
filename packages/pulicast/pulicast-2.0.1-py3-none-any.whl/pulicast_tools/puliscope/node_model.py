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
from typing import List, Dict

from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor

from pulicast.discovery.node_discoverer import NodeDiscoverer
from pulicast.discovery.node_view import NodeView
from pulicast import Node


class NodeModel(QStandardItemModel):
    def __init__(self, node: Node, node_discoverer: NodeDiscoverer):
        super().__init__(0, 2)
        self.setHorizontalHeaderLabels(["Name", "Value"])
        self._node = node
        self._node_discoverer = node_discoverer
        self._node_items_by_id: Dict[int, QStandardItem] = dict()
        self._node_discoverer.add_on_item_added_callback(self._on_new_node)
        self._node_discoverer.add_on_item_removed_callback(self._on_node_left)

        # self.itemChanged.connect(self._on_item_changed)
        self.dataChanged.connect(self._on_data_changed)

    def _on_new_node(self, node_view: NodeView):
        node_item = self.__make_node_item(node_view)
        self._node_items_by_id[node_view.session_id] = node_item
        self.invisibleRootItem().appendRow(node_item)
        node_item.setEditable(False)

        def channel_added(channel_name: str):
            channel_item = QStandardItem(channel_name)
            node_item.appendRow(channel_item)

        node_view.channels.add_on_item_added_callback(channel_added)

    def _on_node_left(self, node_view: NodeView):
        node_item = self._node_items_by_id[node_view.session_id]
        self.removeRow(node_item.row())
        del self._node_items_by_id[node_view.session_id]

    def __make_node_item(self, node_view: NodeView) -> QStandardItem:
        node_item = QStandardItem(node_view.name)
        node_item.setEditable(False)
        node_item.setToolTip(f"Session ID: {node_view.session_id}")
        return node_item

    def _on_data_changed(self, topLeft: QModelIndex, bottomRight: QModelIndex, roles=List):
        # TODO(max): we should solve this by subclassing QStadardModelItem probably
        if Qt.EditRole in roles:
            assert topLeft == bottomRight
            item = self.itemFromIndex(topLeft)
            property_view = item.data()
            print("hi item changed!")
            property_view.set(item.text())