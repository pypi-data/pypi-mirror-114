# !/bin/python3
# Copyright (C) 2020 Kiteswarms GmbH - All Rights Reserved
#
# discovery_api.py
#
# Maximilian Ernestus    [maximilian@kiteswarms.com]
#
# https://www.kiteswarms.com
import trio

from pulicast import TrioNode
from pulicast.discovery.channel_discoverer import ChannelDiscoverer
from pulicast.discovery.channel_view import ChannelView
from pulicast.discovery.node_discoverer import NodeDiscoverer
from pulicast.discovery.node_view import NodeView, Publication
from pulicast_tools.puliconf.setting_discoverer import SettingDiscoverer
from pulicast_tools.puliconf.setting_view import SettingView


async def main():
    async with trio.open_nursery() as nursery:
        node = TrioNode("discoverer", nursery)

        # Setup Node Discoverer
        node_discoverer = NodeDiscoverer(node)

        def announce_node_appeared(node_view: NodeView):
            print(f"node {node_view.name} joined")

        def setup_channel_usage_callbacks(node_view: NodeView):
            # Setup listeners for changes in channel usage
            def announce_new_channel_used(channel_name: str):
                print(f"{node_view.name} now uses {channel_name}")

            def announce_new_subscription(channel_name: str):
                print(f"{node_view.name} now subscribes {channel_name}")

            def announce_new_publication(publication: Publication):
                print(f"{node_view.name} now publishes on {publication.name} with period {publication.period}")

            node_view.channels.add_on_item_added_callback(announce_new_channel_used)
            node_view.subscriptions.add_on_item_added_callback(announce_new_subscription)
            node_view.publications.add_on_item_added_callback(announce_new_publication)

        def announce_node_left(node_view: NodeView):
            print(f"node {node_view.name} left")

        node_discoverer.add_on_item_added_callback(announce_node_appeared)
        node_discoverer.add_on_item_added_callback(setup_channel_usage_callbacks)
        node_discoverer.add_on_item_removed_callback(announce_node_left)

        # Setup Channel Discoverer
        channel_discoverer = ChannelDiscoverer(node_discoverer)

        def announce_new_channel(channel_view: ChannelView):
            print(f"channel {channel_view.name} appeared")

        def announce_channel_disappeared(channel_view: ChannelView):
            print(f"nobody cares for channel {channel_view.name} any more")

        channel_discoverer.add_on_item_added_callback(announce_new_channel)
        channel_discoverer.add_on_item_removed_callback(announce_channel_disappeared)

        # Setup Distributed Settings Discoverer
        setting_discoverer = SettingDiscoverer(node, nursery, node_discoverer)

        def announce_setting_appeared(setting: SettingView):
            print(f"Distributed Setting {setting.name} appeared")

        def announce_setting_disappeared(setting: SettingView):
            print(f"Distributed Setting {setting.name} disappeared")

        setting_discoverer.settings_set.add_on_item_added_callback(announce_setting_appeared)
        setting_discoverer.settings_set.add_on_item_removed_callback(announce_setting_disappeared)

        await node.stopped.wait()


if __name__ == '__main__':
    trio.run(main)