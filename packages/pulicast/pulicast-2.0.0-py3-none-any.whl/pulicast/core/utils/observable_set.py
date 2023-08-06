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
from typing import AbstractSet, Any, Generic, Set, TypeVar, Iterable, Union

from pulicast.core.utils.observable_container import ObservableContainer


T = TypeVar('T')


class ObservableSet(Generic[T], ObservableContainer[T], set):
    def __init__(self, *args, **kwargs):
        ObservableContainer.__init__(self)
        set.__init__(self, *args, **kwargs)

    def add(self, element: T) -> None:
        if element not in self:
            super().add(element)
            self._on_item_added(element)
        else:
            super().add(element)

    def remove(self, element: T) -> None:
        if element in self:
            super().remove(element)
            self._on_item_removed(element)
        else:
            super().remove(element)

    def discard(self, element: T) -> None:
        if element in self:
            super().discard(element)
            self._on_item_removed(element)

    def pop(self) -> T:
        element = super().pop()
        self._on_item_removed(element)
        return element

    def difference_update(self, *s: Iterable[Any]) -> None:
        raise NotImplementedError()
        elements_to_be_removed = self.intersection(s)

    def intersection_update(self, *s: Iterable[Any]) -> None:
        raise NotImplementedError()

    def symmetric_difference_update(self, s: Iterable[T]) -> None:
        elements_to_be_removed = self.intersection(s)
        elements_to_be_added = set(s).difference(self)
        super().symmetric_difference_update(s)
        for element in elements_to_be_removed:
            self._on_item_removed(element)
        for element in elements_to_be_added:
            self._on_item_added(element)

    def update(self, *s: Iterable[T]) -> None:
        elements_to_be_added = set(*s).difference(self)
        super().update(*s)
        for element in elements_to_be_added:
            self._on_item_added(element)

    def __iand__(self, s: AbstractSet[object]) -> 'ObservableSet[T]':
        self.intersection_update(s)
        return self

    def __isub__(self, s: AbstractSet[object]) -> 'ObservableSet[T]':
        self.difference_update(s)
        return self

    def __ixor__(self, s: AbstractSet) -> 'ObservableSet[T]':
        self.symmetric_difference_update(s)
        return self





