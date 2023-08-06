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
from pulicast import Channel
from pulicast.namespace import Namespace


def is_setting_confirmation_channel(channel_name: str) -> bool:
    """Checks if a channel is a distributed setting's confirmation channel."""
    return ".config/" in channel_name and not channel_name.endswith(".r")


def is_setting_roc_channel(channel_name: str) -> bool:
    """Checks if a channel is a request of change channel of a distributed setting."""
    return ".config/" in channel_name and channel_name.endswith(".r")


def deduce_roc_channel_from_confirmation_channel(confirmation_channel_name: str) -> str:
    """Deduces the request of change channel name from a confirmation channel name."""
    assert is_setting_confirmation_channel(confirmation_channel_name), f"The given channel name ({confirmation_channel_name}) is not a setting confirmation channel"
    return confirmation_channel_name + ".r"


def deduce_confirmation_channel_from_roc_channel(roc_channel_name: str) -> str:
    """Deduces the confirmation channel name from a roc channel name."""
    assert is_setting_roc_channel(roc_channel_name), f"The given channel name ({roc_channel_name}) is not a request of change (ROC) channel name."
    return roc_channel_name[:-2]


def deduce_setting_name_from_confirmation_channel(confirmation_channel_name: str) -> str:
    """Deduces the name of a setting from its confirmation channel name."""
    assert is_setting_confirmation_channel(confirmation_channel_name), f"The given channel name ({confirmation_channel_name}) is not a setting confirmation channel name."
    return confirmation_channel_name.replace(".config/", "")


def obtain_roc_channel_from_name(name: str, ns: Namespace) -> Channel:
    return (ns / ".config")[name + ".r"]


def obtain_confirmation_channel_from_name(name: str, ns: Namespace) -> Channel:
    return (ns / ".config")[name]
