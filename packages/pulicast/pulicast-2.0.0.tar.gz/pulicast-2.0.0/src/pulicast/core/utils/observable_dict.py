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
from typing import TypeVar, Generic, overload

from pulicast.core.utils.observable_container import ObservableContainer

T = TypeVar('T')
K = TypeVar('K')


class ObservableDict(Generic[K, T], ObservableContainer[T], dict):
    """
    A map whose contents is observable by inheriting from :class:`.ObservableContainer`.
    """

    def __init__(self, *args, **kwargs) -> None:
        ObservableContainer.__init__(self)
        dict.__init__(self, *args, **kwargs)
        # super(ObservableContainer).__init__()
        # super(dict).__init__(*args, **kwargs)

    def __setitem__(self, key: K, value: T):
        if key not in self:
            super().__setitem__(key, value)
            self._on_item_added(value)

    def pop(self, key: K):
        return self._on_item_removed(super().pop(key))

    def __delattr__(self, key: K):
        self.pop(key)

    def __iter__(self):
        return self.values().__iter__()

    def clear(self) -> None:
        # Note: self.keys() returns an iterator, that would be invalidated when deleting entries.
        # Therefore we need to convert it to a tuple before iteration.
        for key in tuple(self.keys()):
            del self[key]

    def popitem(self):
        raise NotImplementedError()

    @overload
    def update(self, **kwargs):
        raise NotImplementedError()

    def __delitem__(self, key: K):
        self.pop(key)

