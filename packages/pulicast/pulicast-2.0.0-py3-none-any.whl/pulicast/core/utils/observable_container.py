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
from typing import TypeVar, Generic, Callable, List

T = TypeVar('T')


class ObservableContainer(Generic[T]):
    """
    An abstract container class with support for registering a callback for whenever an item is added or removed.
    """

    def __init__(self):
        self._on_item_added_callbacks: List[Callable[[T], None]] = []
        self._on_item_removed_callbacks: List[Callable[[T], None]] = []

    def add_on_item_added_callback(self, callback: Callable[[T], None], call_on_existing_items: bool = True):
        """
        Register a callback for whenever an item is added to the container.

        .. note::
            This will call the callback on the already existing items
            unless suppressed by setting ``call_on_existing_items`` to ``False``.

        :param callback: The function to call when an item has been added.
        :param call_on_existing_items: Whether to call the function on the already existing items or not.
            True by default.
        """
        self._on_item_added_callbacks.append(callback)
        if call_on_existing_items:
            for item in self:
                callback(item)

    def remove_on_item_added_callback(self, callback: Callable[[T], None]):
        self._on_item_added_callbacks.remove(callback)

    def add_on_item_removed_callback(self, callback: Callable[[T], None]):
        """
        Register a callback for whenever an item has been removed from the container.

        :param callback: The function to call when an item has been removed.
        """
        self._on_item_removed_callbacks.append(callback)

    def remove_on_item_removed_callback(self, callback: Callable[[T], None]):
        self._on_item_removed_callbacks.remove(callback)

    def is_observed(self) -> bool:
        """Checks whether any callbacks have been registered on this observable container."""
        return len(self._on_item_added_callbacks) + len(self._on_item_removed_callbacks) > 0

    def _on_item_added(self, item: T):
        for cb in self._on_item_added_callbacks:
            cb(item)

    def _on_item_removed(self, item: T):
        for cb in self._on_item_removed_callbacks:
            cb(item)
