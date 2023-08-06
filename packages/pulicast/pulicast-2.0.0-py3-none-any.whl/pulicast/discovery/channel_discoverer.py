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

from pulicast.discovery.channel_view import ChannelView
from pulicast.discovery.node_discoverer import NodeDiscoverer
from pulicast.discovery.node_view import NodeView, Publication
from pulicast.core.utils.observable_dict import ObservableDict


class ChannelDiscoverer(ObservableDict[str, ChannelView]):
    """
    The :class:`.ChannelDiscoverer` is an :class:`.ObservableMap`, that will contain a :class:`.ChannelView`
    for each channel that is somehow in use within the pulicast network.
    """

    def __init__(self, node_discoverer: NodeDiscoverer):
        super().__init__()

        node_discoverer.add_on_item_added_callback(self._on_node_added)
        node_discoverer.add_on_item_removed_callback(self._on_node_left)

    def _on_node_added(self, node_view: NodeView):

        # Handle new subscriptions
        def subscription_added(channel_name: str):
            if channel_name not in self:
                self[channel_name] = ChannelView(channel_name)
            self[channel_name].subscribers.add(node_view)
        for subscription in node_view.subscriptions:
            subscription_added(subscription)

        node_view.subscriptions.add_on_item_added_callback(subscription_added)

        # Handle new publications
        def publication_added(publication: Publication):
            channel_name = publication.name
            if channel_name not in self:
                self[channel_name] = ChannelView(channel_name)
            self[channel_name].publishers.add(node_view)

        for publication in node_view.publications:
            publication_added(publication)

        node_view.publications.add_on_item_added_callback(publication_added)

        # Handle new general channel usages
        def channel_added(channel_name: str):
            if channel_name not in self:
                self[channel_name] = ChannelView(channel_name)
            self[channel_name].nodes.add(node_view)
        for channel in node_view.channels:
            channel_added(channel)

        node_view.channels.add_on_item_added_callback(channel_added)


    def _on_node_left(self, node_view: NodeView):
        for channel_name in node_view.subscriptions:
            channel_view = self[channel_name]
            channel_view.subscribers.remove(node_view)
            if len(channel_view.subscribers) == 0 and len(channel_view.publishers) == 0:
                del self[channel_name]

        for publication in node_view.publications:
            channel_view = self[publication.name]
            channel_view.publishers.remove(node_view)
            if len(channel_view.subscribers) == 0 and len(channel_view.publishers) == 0:
                del self[publication.name]
