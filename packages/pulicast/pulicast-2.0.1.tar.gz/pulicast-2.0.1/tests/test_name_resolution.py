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
import pytest

from pulicast.core.utils.name_resolution import resolve_name


@pytest.mark.parametrize("name", ["", "a", "asd", "asd1/asd2", "asd1/asd2/"])
@pytest.mark.parametrize("namespace", ["", "/ns", "ns/", "ns1/ns2"])
def test_that_slash_prefix_causes_global_lookup(name: str, namespace: str):
    # WHEN
    resolved_name = resolve_name("/" + name, namespace)

    # THEN
    assert resolved_name == name.strip("/")


@pytest.mark.parametrize("name", ["", "a", "asd", "asd1/asd2", "asd1/asd2/"])
@pytest.mark.parametrize("namespace", ["", "/ns", "ns/", "ns1/ns2"])
def test_that_namespace_becomes_prefix(name: str, namespace: str):
    # WHEN
    resolved_name = resolve_name(name, namespace)
    resolved_namespace = resolve_name(namespace)  # Note: this removes any leading or trailing slashes from the namespace

    # THEN
    assert resolved_name.startswith(resolved_namespace)


@pytest.mark.parametrize("name", ["", "a", "asd", "asd1/asd2", "asd1/asd2/"])
@pytest.mark.parametrize("namespace", ["", "/ns", "ns/", "ns1/ns2"])
def test_that_name_becomes_postfix(name: str, namespace: str):
    # WHEN
    resolved_name = resolve_name(name, namespace)
    root_resolved_name = resolve_name(name, "/")  # Note: this removes any leading or trailing slashes

    # THEN
    assert resolved_name.endswith(root_resolved_name)


def test_that_relative_names_are_resolved():
    # Switch to parent ns
    assert resolve_name("../channel", namespace="l1/") == "channel"
    assert resolve_name("../channel", namespace="l1/l2") == "l1/channel"
    assert resolve_name("../../channel", namespace="l1/l2") == "channel"

    # Switch to sibling ns
    assert resolve_name("../l3/channel", namespace="l1/l2") == "l1/l3/channel"

    # Switching beyond root falls back to root
    assert resolve_name("../channel", namespace="/") == "channel"
    assert resolve_name("../../channel", namespace="/l1") == "channel"
    assert resolve_name("../l2/../../channel", namespace="/l1") == "channel"


def test_that_relative_namespaces_are_resolved():
    # Switch to parent ns
    assert resolve_name("channel", namespace="l1/..") == "channel"
    assert resolve_name("channel", namespace="l1/l2/..") == "l1/channel"
    assert resolve_name("channel", namespace="l1/l2/../..") == "channel"

    # Switch to sibling ns
    assert resolve_name("channel", namespace="l1/../l2") == "l2/channel"

    # Switching beyond root falls back to root
    assert resolve_name("channel", namespace="l1/../..") == "channel"


def test_that_double_slashes_are_ignored():
    assert resolve_name("..//channel", namespace="l1/") == "channel"
    assert resolve_name("//channel", namespace="l1/") == "channel"
    assert resolve_name("../..//channel", namespace="l1/l2") == "channel"
