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
from typing import Any, Callable, Iterable, Tuple, Type, Union

import pytest

from pulicast.core.utils.observable_set import ObservableSet


def call_and_record_return_and_exception_type(fun: Callable, args=()) -> Tuple[Any, Type]:
    """
    Calls a function and records its return value or raised exception type.

    :param fun: The function to call.
    :param args: The arguments to pass to the function to call (only varargs supported now kwargs).
    :return: A tuple (return, exception type)
    """
    ret = None
    exception_type = None
    try:
        ret = fun(*args)
    except Exception as e:
        exception_type = type(e)
    return ret, exception_type


def check_set_behaves_like_observable_set(set_elements: Iterable,
                                          operation: Union[str, Callable[[Union[set, ObservableSet], Iterable], Any]],
                                          args=()):
    """
    Check that an operation behaves on a set exactly like on an observable set. Also checks if the on item added and
    removed callbacks are called correctly.

    For this the need to have the same return value, throw the same exception type and have the same elements after
    applying the operation.

    :param set_elements: The elements in the sets with wich to start with.
    :param operation: The operation to apply to the sets. Can either be a name of a member function of both set and
    ObservableSet or a callable taking a set/ObservableSet and the other arguments.
    :param args: The arguments to pass to the operation.
    """
    # GIVEN
    o_set = ObservableSet(set_elements)
    uo_set = set(set_elements)

    # Normalize the operation
    if isinstance(operation, str):
        o_operation = getattr(o_set, operation)
        uo_operation = getattr(uo_set, operation)
    else:
        o_operation = lambda a: operation(o_set, a)
        uo_operation = lambda a: operation(uo_set, a)

    # Record the observable set callback
    added_elements_record = set()
    removed_elements_record = set()

    def on_element_added_cb(e):
        added_elements_record.add(e)

    o_set.add_on_item_added_callback(on_element_added_cb, False)
    o_set.add_on_item_removed_callback(lambda e: removed_elements_record.add(e))

    # WHEN
    uo_ret, uo_exception = call_and_record_return_and_exception_type(uo_operation, args)
    o_ret, o_exception = call_and_record_return_and_exception_type(o_operation, args)

    # THEN
    assert o_exception == uo_exception
    assert o_ret == uo_ret
    assert o_set == uo_set

    elements_that_have_been_added = o_set - set(set_elements)
    elements_that_have_been_removed = set(set_elements) - o_set
    assert elements_that_have_been_added == added_elements_record
    assert elements_that_have_been_removed == removed_elements_record


@pytest.mark.parametrize("operation", ["add", "remove", "discard"])
@pytest.mark.parametrize("element", ["A", "X", None])
@pytest.mark.parametrize("set_elements", [[], ["A"], [None], ["A", None], ["A", "B"]])
def test_element_operation(operation, element, set_elements):
    check_set_behaves_like_observable_set(set_elements, operation, (element,))


@pytest.mark.parametrize("set_elements", [[], ["A"], [None], ["A", None], ["A", "B"]])
def test_pop(set_elements):
    check_set_behaves_like_observable_set(set_elements, "pop")


@pytest.mark.parametrize("lhs_elements", [[], ["A"], [None], ["A", None], ["A", "B"], ["A", "B", "C"], ["X"]])
@pytest.mark.parametrize("rhs_elements", [[], ["A"], [None], ["A", None], ["A", "B"], ["A", "B", "C"], ["X"]])
def test_symmetric_difference_update_operation(lhs_elements, rhs_elements):
    check_set_behaves_like_observable_set(lhs_elements, "symmetric_difference_update", [rhs_elements])

@pytest.mark.parametrize("lhs_elements", [[], ["A"], [None], ["A", None], ["A", "B"], ["A", "B", "C"], ["X"]])
@pytest.mark.parametrize("rhs_elements", [[], ["A"], [None], ["A", None], ["A", "B"], ["A", "B", "C"], ["X"]])
def test_symmetric_difference_update_operation(lhs_elements, rhs_elements):
    def apply_inline_xor(s, args):
        s ^= set(args)

    check_set_behaves_like_observable_set(lhs_elements, apply_inline_xor, [rhs_elements])


@pytest.mark.parametrize("lhs_elements", [[], ["A"], [None], ["A", None], ["A", "B"], ["A", "B", "C"], ["X"]])
@pytest.mark.parametrize("rhs_elements", [[], ["A"], [None], ["A", None], ["A", "B"], ["A", "B", "C"], ["X"]])
def test_update_operation(lhs_elements, rhs_elements):
    check_set_behaves_like_observable_set(lhs_elements, "update", [rhs_elements])
