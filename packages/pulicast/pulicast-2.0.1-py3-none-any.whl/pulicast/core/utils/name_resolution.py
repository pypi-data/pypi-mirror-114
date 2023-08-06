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
#     along with pulicast.  If not, see <https://www.gnu.org/licenses/>.m
import pathlib
import posixpath


def resolve_name(name: str, namespace: str = "/") -> str:
    """
    Resolves the name of a pulicast channel or node within the given namespace.

    See the documentation on name resolution for details on how names are resolved exactly.

    :param name: The name to resolve.
    :param namespace: The namespace we are in. "/" is the root.
    :return: The resolved name.
    """
    normalized_namespace = posixpath.normpath(pathlib.PurePosixPath("/", namespace))
    resolved_name = posixpath.normpath(pathlib.PurePosixPath(normalized_namespace, name))
    return resolved_name.strip("/")
