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
from typing import Union

from PySide2.QtCore import QUrl, Signal, QObject
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QApplication
from graphviz import Digraph

from pulicast.channel_naming_conventions import is_hidden_channel
from pulicast.discovery.channel_discoverer import ChannelDiscoverer
from pulicast.discovery.channel_view import ChannelView
from pulicast.discovery.node_discoverer import NodeDiscoverer
from pulicast.discovery.node_view import NodeView

class PuligraphWidget(QWebEngineView):
    element_hovered = Signal((NodeView,), (ChannelView,), (str,), ())
    element_clicked = Signal((NodeView,), (ChannelView,), (str,), ())
    channel_clicked = Signal(ChannelView)
    
    _channel_prefix = "channel_"
    _node_prefix = "node_"
    _usage_prefix = "usage_"


    def __init__(self, node_discoverer: NodeDiscoverer, parent=None):
        super(PuligraphWidget, self).__init__(parent=parent)

        self._node_discoverer = node_discoverer

        self._node_discoverer.add_on_item_added_callback(self._on_change)
        self._node_discoverer.add_on_item_added_callback(self._on_new_node)
        self._node_discoverer.add_on_item_added_callback(lambda i: print(f"Node joined: {i.name}"))

        self._node_discoverer.add_on_item_removed_callback(self._on_change)
        self._node_discoverer.add_on_item_removed_callback(lambda i: print(f"Node left: {i.name}"))

        self.urlChanged.connect(self._on_element_clicked)
        self.page().linkHovered.connect(self._on_element_hovered)
        
        self.channel_discoverer = ChannelDiscoverer(node_discoverer)


    def _on_new_node(self, node_view: NodeView):
        node_view.publications.add_on_item_added_callback(self._on_change, False)
        node_view.subscriptions.add_on_item_added_callback(self._on_change, False)

    def _on_change(self, _):
        graph = self.graph_from_discoverer()
        self._set_graph(graph)

    def graph_from_discoverer(self) -> Digraph:
        graph = Digraph(engine="dot")
        font = QApplication.font().family()
        graph.node_attr["fillcolor"] = "white"
        graph.node_attr["style"] = "filled"
        graph.node_attr["fontname"] = font
        graph.node_attr["shape"] = "none"

        graph.graph_attr["fontname"] = font
        graph.graph_attr["center"] = "1"

        if graph.engine == "neato":
            graph.graph_attr["overlap"] = "false"


        if graph.engine == "twopi":
            graph.graph_attr["center"] = "true"
            # graph.graph_attr["root"] = "__nodes"
            graph.graph_attr["overlap"] = "false"
            graph.graph_attr["ranksep"] = "3"



        graph.edge_attr["fontname"] = font

        for node in self._node_discoverer:
            if "bridge" in node.name:
                continue
            graph.node(str(node.session_id), href=f"#{self._node_prefix}{node.session_id}", label=node.name)

            for channel_name in filter(lambda n: not is_hidden_channel(n), node.channels):
            # for channel_name in node.channels:
                graph.node(channel_name, href=f"#{self._channel_prefix}{channel_name}", shape="oval")

                if channel_name in node.subscriptions:
                    graph.edge(channel_name, str(node.session_id), href=f"#{self._usage_prefix}{str(node.session_id)}_{channel_name}")

                if channel_name in node.publications:
                    graph.edge(str(node.session_id), channel_name, href=f"#{self._usage_prefix}{str(node.session_id)}_{channel_name}")

                if channel_name not in node.subscriptions and channel_name not in node.publications:
                    graph.edge(str(node.session_id), channel_name,
                               href=f"#{self._usage_prefix}{str(node.session_id)}_{channel_name}",
                               style="dotted")

        return graph

    def _set_graph(self, graph: Digraph):
        self.setContent(graph.pipe(format="svg"), mimeType="image/svg+xml", baseUrl=QUrl("file://"))

    def _on_element_hovered(self, link: str):
        element = self._get_element_from_url(QUrl(link))
        self.element_hovered.emit(element)

    def _on_element_clicked(self, element_url: QUrl):
        element = self._get_element_from_url(element_url)
        self.element_clicked.emit(element)
        if type(element) == ChannelView:
            self.channel_clicked.emit(element)
        print("Clicked", element)

    def _get_element_from_url(self, url: QUrl) -> Union[NodeView, str, ChannelView, None]:
        if url.hasFragment():
            if url.fragment().startswith(self._channel_prefix):
                channel_id = url.fragment()[len(self._channel_prefix):]
                return self.channel_discoverer[channel_id]
            elif url.fragment().startswith(self._node_prefix):
                node_id = int(url.fragment()[len(self._node_prefix):])
                return self._node_discoverer[node_id]
            elif url.fragment().startswith(self._usage_prefix):
                usage_string = url.fragment()[len(self._usage_prefix):]
                node_id_end = usage_string.find("_", len(self._usage_prefix))
                node_id = int(usage_string[:node_id_end])
                channel_name = usage_string[node_id_end+1:]
                return (node_id, channel_name)
        return None








