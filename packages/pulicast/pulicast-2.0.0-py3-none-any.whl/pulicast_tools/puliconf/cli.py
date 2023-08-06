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
from collections import OrderedDict
from typing import Dict

import click
import qtrio
import tomlkit
import trio
from PySide2.QtNetwork import QNetworkInterface
from PySide2.QtNetwork import QAbstractSocket
from PySide2.QtWidgets import QApplication

import pulicast
from pulicast import Node, QtNode
from pulicast.discovery.node_discoverer import NodeDiscoverer
from pulicast_tools.puliconf.setting_discoverer import SettingDiscoverer
from pulicast_tools.puliconf.utils import convert_settings_to_toml, diff_configuration, pull_configuration, \
    push_configuration


def get_network_interface_lookup_dict() -> Dict[str, QNetworkInterface]:
    """
    Creates a dictionary mapping ipv4 addresses and interface names to QNetworkInterface instances, that are currently up.
    """
    def get_ipv4_address_strings(iface: QNetworkInterface):
        return [e.ip().toString() for e in iface.addressEntries() if e.ip().protocol() == QAbstractSocket.IPv4Protocol]

    all_interfaces_that_are_up = [i for i in QNetworkInterface.allInterfaces() if i.flags() & QNetworkInterface.IsUp]

    interface_lookup_dict = OrderedDict()
    for iface in all_interfaces_that_are_up:
        interface_lookup_dict[iface.name()] = iface
        for address_string in get_ipv4_address_strings(iface):
            interface_lookup_dict[address_string] = iface
    return interface_lookup_dict


@click.group()
@click.option("-p", "--port", type=click.IntRange(1, 2**16-1), default=pulicast.DEFAULT_PORT,
              help="The pulicast port to listen on.", show_default=True)
@click.option("-i", "--interface", type=click.Choice(list(get_network_interface_lookup_dict())),
              help="The name or address of the network interface to use for joining multicast groups.")
@click.option("-t", "--ttl", type=click.IntRange(0, 2**8), default=0, show_default=True,
              help="The `time to live <https://en.wikipedia.org/wiki/Time_to_live>`_ for messages being sent. "
                    "Set to 0 to keep the traffic on the local machine.")
@click.pass_context
def cli(ctx, port, interface, ttl):
    """A tool to read and write pulicast distributed settings."""
    # Note: we need to create a QApplication before creating a QtNode. Later qtrio will reuse that application
    app = QApplication()
    ctx.obj = QtNode("puliconf", port=port, ttl=ttl, interface=get_network_interface_lookup_dict().get(interface, None))


@cli.command(short_help="read configuration")
@click.argument("config_file", type=click.File('w', lazy=True), default="-")
@click.pass_context
def pull(ctx, config_file):
    """
    Reads all distributed settings and prints them or writes them to CONFIG_FILE if specified.

    Note: will wait for new distributed settings to be discovered until no one was newly discovered for 2s.

    Note: the TOML file format is used with NaN values designating uninitialized/None settings and a special field named
    __msg_type__ to encode the value type of a setting.
    """
    async def do_pull():
        async with trio.open_nursery() as nursery:
            node = ctx.find_object(Node)

            discoverer = NodeDiscoverer(node)
            setting_discoverer = SettingDiscoverer(node, nursery, discoverer)
            toml_doc = await pull_configuration(setting_discoverer.settings_set)

            if len(toml_doc) > 0:
                config_file.write(tomlkit.dumps(toml_doc))

            logging.info(f"Pulled {len(toml_doc)} settings.")

    qtrio.run(do_pull)


@cli.command(short_help="apply configuration changes")
@click.option("--reset-first", is_flag=True, type=bool, default=False,
              help="Resets each distributed setting to its default value before applying the value in the config file.")
@click.option("--unset-first", is_flag=True, type=bool, default=False,
              help="Unsets each distributed setting before applying the value in the config file.")
@click.argument("config_file", type=click.File('r'))
@click.argument("changes_file", type=click.File('w', lazy=True), default="-")
@click.pass_context
def push(ctx, reset_first, unset_first, config_file, changes_file):
    """
    Sets all distributed settings to the values specified in the CONFIG_FILE.
    Then prints the applied changes or writes them to the CHANGES_FILE if specified.
    If a distributed setting was already set to the value specified in the CONFIG_FILE, it will not appear in the
    CHANGES_FILE.
    If some settings failed to be set, no CHANGES_FILE will be generated.

    Note: will wait for new distributed settings to be discovered until no one was newly discovered for 2s.
    """
    async def do_push():
        async with trio.open_nursery() as nursery:
            node = ctx.find_object(Node)

            discoverer = NodeDiscoverer(node)
            setting_discoverer = SettingDiscoverer(node, nursery, discoverer)
            toml_doc = tomlkit.parse(config_file.read())

            changed_settings, unchanged_settings, failed_settings = \
                await push_configuration(setting_discoverer.settings_set, toml_doc, reset_first, unset_first)

            if len(changed_settings) > 0 and len(failed_settings) == 0:
                print(f"# Minimal set of changes:")
                changes_file.write(tomlkit.dumps(convert_settings_to_toml(changed_settings)))

    qtrio.run(do_push)


@cli.command(short_help="generate diff between current configurtion and config file")
@click.argument("config_file", type=click.File('r'))
@click.argument("diff_output", type=click.File('w', lazy=True), default="-")
@click.pass_context
def diff(ctx, config_file, diff_output):
    """
    Generates a diff between the current configuration and a CONFIG_FILE in the form of a TOML file, that could be
    applied using `puliconf push`. Prints that TOML file or writes it to DIFF_OUTPUT if specified.
    """
    async def do_diff():
        async with trio.open_nursery() as nursery:
            node = ctx.find_object(Node)

            discoverer = NodeDiscoverer(node)
            setting_discoverer = SettingDiscoverer(node, nursery, discoverer)
            toml_doc = tomlkit.parse(config_file.read())

            diff_doc = await diff_configuration(setting_discoverer.settings_set, toml_doc)
            if len(diff_doc) > 0:
                diff_output.write(tomlkit.dumps(diff_doc))

    qtrio.run(do_diff)


if __name__ == '__main__':
    cli()