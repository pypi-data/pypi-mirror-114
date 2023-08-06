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
from typing import Generic, TypeVar, Callable, Set, Any, Type, Dict

T = TypeVar('T')


class ObservableProperty(Generic[T]):
    """
    A variant of the python property that can be observed for changes.

    Beware! Not to be confused with pulicast properties or their views!

    Usage example:

    >>> class MyClass: watchable_flag = ObservableProperty(False)
    >>> my_obj1 = MyClass()
    >>> my_obj2 = MyClass()
    >>> my_obj1.watchable_flag
    False
    >>> my_obj2.watchable_flag
    False

    >>> MyClass.watchable_flag.add_on_changed_callback(my_obj1, lambda f: print(f"flag of obj1 changed to {f}"))
    >>> my_obj1.watchable_flag = False
    >>> my_obj1.watchable_flag = True
    flag of obj1 changed to True
    >>> my_obj1.watchable_flag
    True
    >>> my_obj2.watchable_flag
    False
    """

    def __init__(self, initial_value: T):
        self._values: Dict[Any, T] = dict()
        self._initial_value = initial_value
        self._on_change_callbacks: Dict[Any, Set[Callable[[T], None]]] = dict()

    def __set__(self, obj: Any, new_value: T):
        if new_value != self._values.get(obj, self._initial_value):
            self._values[obj] = new_value
            self._dispatch_callbacks(obj, new_value)

    def __get__(self, obj: Any, objtype: Type):
        if obj is None:
            return self
        else:
            return self._values.get(obj, self._initial_value)

    def _dispatch_callbacks(self, obj, new_value):
        for cb in self._on_change_callbacks.get(obj, []):
            cb(new_value)

    def add_on_changed_callback(self, obj: Any, callback: Callable[[T], None]):
        """
        Add a callback to be called when the property changes.

        :param obj: The object on which to watch the property.
        :param callback: The function to call when the property changes.
        """
        if obj not in self._on_change_callbacks:
            self._on_change_callbacks[obj] = set()
        self._on_change_callbacks[obj].add(callback)

    def add_on_changed_to_callback(self, obj: Any, callback: Callable[[], None], target_value: T):
        """
        Add a callback to be called when the property changes to a specific value.

        This is especially useful when observing boolean properties.

        :param obj: The object on which to watch the property.
        :param callback: The function to call when the property changes to the target value.
        :param target_value: The value to wait for.
        """
        def call_callback_if_target_value_reached(new_value: T):
            if new_value == target_value:
                callback()
        self.add_on_changed_callback(obj, call_callback_if_target_value_reached)