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
import PySide2
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QMainWindow, QDockWidget, QTreeView
from trio import Nursery

from pulicast import Node
from pulicast.discovery.node_discoverer import NodeDiscoverer
from pulicast_tools.puliconf.setting_discoverer import SettingDiscoverer
from pulicast_tools.puliscope.node_model import NodeModel
from pulicast_tools.puliscope.puligraph_widget import PuligraphWidget
from pulicast_tools.puliscope.pulijit_widget import PulijitWidget
from pulicast_tools.puliscope.settings_model import SettingsModel


class MainWindow(QMainWindow):

    closed = Signal()

    def __init__(self, node: Node, nursery: Nursery):
        super().__init__()

        node_discoverer = NodeDiscoverer(node)
        setting_discoverer = SettingDiscoverer(node, nursery, node_discoverer)

        self.setWindowTitle("Puliscope")
        graph_widget = PuligraphWidget(node_discoverer, self)
        self.setCentralWidget(graph_widget)

        node_model = NodeModel(node, node_discoverer)
        node_widget = QTreeView()
        node_widget.setModel(node_model)
        node_dock = QDockWidget()
        node_dock.setWidget(node_widget)

        setting_model = SettingsModel(node, nursery, setting_discoverer)
        setting_widget = QTreeView()
        setting_widget.setModel(setting_model)
        setting_dock = QDockWidget()
        setting_dock.setWidget(setting_widget)

        jitter_widget = PulijitWidget(node, node_discoverer, self)
        jitter_dock = QDockWidget()
        jitter_dock.setWidget(jitter_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, jitter_dock)
        # When a channel is clicked in the graph widget, pulijit subscribe to it
        graph_widget.channel_clicked.connect(jitter_widget.subscribe)

        self.addDockWidget(Qt.RightDockWidgetArea, node_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, setting_dock)

    def closeEvent(self, event:PySide2.QtGui.QCloseEvent) -> None:
        self.closed.emit()

