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
import math
import warnings
from typing import Callable, Generic, Optional, Tuple, TypeVar


from pulicast.namespace import Namespace
from pulicast.serialization import get_message_encoder
from pulicast_messages import poke_setting, reset_setting_to_default, roc_ack, unset_setting
from pulicast_tools.puliconf.channel_naming_conventions import obtain_confirmation_channel_from_name, obtain_roc_channel_from_name, \
    deduce_setting_name_from_confirmation_channel
from pulicast_tools.puliconf.setting_view import zcm_msg_equals

T = TypeVar('T')

ValidationFunction = Callable[[Optional[T]], Tuple[str, bool]]


def accept_everything() -> ValidationFunction[T]:
    return lambda value: ("", True)


def accept_nothing() -> ValidationFunction[T]:
    return lambda value: ("static value is read-only", False)


def accept_only(*acceptable_values) -> ValidationFunction[T]:
    acceptable_values = set(acceptable_values)

    def accept_if_in_values(roc: Optional[T]):
        if roc is not None and roc in acceptable_values:
            return "", True
        else:
            return f"must be in {acceptable_values}", False

    return accept_if_in_values


def accept_at_least(minimum: T) -> ValidationFunction[T]:
    def accept_if_large_enough(roc: Optional[T]):
        if roc is not None and minimum <= roc:
            return "", True
        else:
            return f"must be at least {minimum}", False

    return accept_if_large_enough


def accept_at_most(maximum: T) -> ValidationFunction[T]:
    def accept_if_small_enough(roc: Optional[T]):
        if roc is not None and roc <= maximum:
            return "", True
        else:
            return f"bust be at most {maximum}", False

    return accept_if_small_enough


def accept_above(v: T) -> ValidationFunction[T]:
    def accept_if_large_enough(roc: Optional[T]):
        if roc is not None and v < roc:
            return "", True
        else:
            return f"must be above {v}", False

    return accept_if_large_enough


def accept_at_below(v: T) -> ValidationFunction[T]:
    def accept_if_small_enough(roc: Optional[T]):
        if roc is not None and roc < v:
            return "", True
        else:
            return f"bust be below {v}", False

    return accept_if_small_enough


def accept_range(minimum: T, maximum: T) -> ValidationFunction[T]:
    def accept_if_in_range(roc: Optional[T]):
        if roc is not None and minimum <= roc <= maximum:
            return "", True
        else:
            return f"must be in [{minimum}, {maximum}]", False

    return accept_if_in_range


def accept_in_interval(min_v=-math.inf, max_v=math.inf, all_above=-math.inf, all_below=math.inf) -> ValidationFunction[T]:
    """
    Produces an acceptor, that accepts valus from the given interval.


    :param min_v: All values must be larger or equal to min_v.
    :param max_v: All values must be smaller or equal to max_v.
    :param all_above: All values must be strictly larger than all_above.
    :param all_below: All values must be strictly smaller than all_below.
    :return:

    >>> half_open_i = accept_in_interval(all_above=5, max_v=7)
    >>> print(half_open_i.__doc__)
    Value must be in (5, 7]!
    >>> half_open_i(6)[1]
    True
    >>> half_open_i(5)[1]
    False
    >>> half_open_i(5.00000001)[1]
    True
    >>> half_open_i(7)[1]
    True
    >>> half_open_i(7.00000001)[1]
    False
    >>> open_i = accept_in_interval(all_below=10, all_above=-10)
    >>> print(open_i.__doc__)
    Value must be in (-10, 10)!
    >>> open_i(10)[1]
    False
    >>> open_i(-10)[1]
    False
    >>> open_i(0)[1]
    True
    >>> open_i(9.999)[1]
    True
    >>> open_i(-9.999)[1]
    True
    >>> closed_i = accept_in_interval(min_v=0, max_v=5)
    >>> print(closed_i.__doc__)
    Value must be in [0, 5]!
    >>> closed_i(0)[1]
    True
    >>> closed_i(5)[1]
    True
    >>> closed_i(-0.000001)[1]
    False
    >>> closed_i(5.00001)[1]
    False
    """

    if not all_above <= all_below:
        raise ValueError("You must ensure that all_above < all_below. This is not given since it is not valid "
                         f"that {all_above} < {all_below}")

    if not min_v <= max_v:
        raise ValueError("You must ensure that min_v <= max_v. This is not given since it is not valid "
                         f"that {min_v} <= {max_v}")

    is_left_closed = all_above < min_v
    is_right_closed = max_v < all_below

    description_str = f"must be in {f'[{min_v}' if is_left_closed else f'({all_above}'}, {f'{max_v}]' if is_right_closed else f'{all_below})'}"

    def check_in_range(roc: Optional[T]):
        is_in_range = roc is not None and all_above < roc < all_below and min_v <= roc <= max_v
        return ("", True) if is_in_range else (description_str, False)
    check_in_range.__doc__ = description_str
    return check_in_range


class Setting(Generic[T]):
    def __init__(self, name: str, namespace: Namespace, initial_value=None, value_type=None,
                 value_changed: Callable[[], None] = lambda: None,
                 validate_roc: ValidationFunction = accept_everything()):
        if initial_value is not None and value_type is not None:
            if type(initial_value) == value_type:
                warnings.warn(f"Initial value and value type of {name} were both specified. "
                              f"This is redundant and therefore should be avoided.")
            else:
                raise ValueError(f"Specified type {value_type} for {name} while its initial value {initial_value} is "
                                 f"of type {type(initial_value)}!")

        if initial_value is None and value_type is None:
            raise ValueError("You either need to pass an initial value or a value type to a setting!")

        if value_type is None:
            value_type = type(initial_value)

        self._value_type = value_type
        self._value = initial_value
        self._value_changed_callback = value_changed
        self._confirmation_channel = obtain_confirmation_channel_from_name(name, namespace)

        roc_channel = obtain_roc_channel_from_name(name, namespace)
        assert not roc_channel.is_subscribed, "The setting already seems to exist since the roc channel is already " \
                                              "subscribed!"
        assert not self._confirmation_channel.is_published, "The setting already seems to exist since its channel is " \
                                                            "already published!"

        # define message handlers
        def handle_roc(roc: value_type):
            warning, accepted = validate_roc(roc)

            if accepted:
                self._set_value(roc)

            self._send_confirmation(warning)

        def handle_poke(_: poke_setting):
            warning, _ = validate_roc(None)
            self._send_confirmation(warning)

        def handle_unset(_: unset_setting):
            handle_roc(None)

        def handle_reset(_: reset_setting_to_default):
            handle_roc(initial_value)

        # register message handlers
        roc_channel.subscribe(handle_roc)
        roc_channel.subscribe(handle_poke)
        roc_channel.subscribe(handle_unset)
        roc_channel.subscribe(handle_reset)

        # Note: this initial call to handle_poke causes us to publish on the confirmation channel.
        # This makes it easier for a settings discoverer to discover this setting: When a node subscribes to the
        # request channel AND publishes on the confirmation channel this is a good indicator, that it owns the setting.
        handle_poke(None)

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return deduce_setting_name_from_confirmation_channel(self._confirmation_channel.name)

    def get(self, default: Optional[T] = None):
        return default if self._value is None else self._value

    def _set_value(self, new_value: T):
        if zcm_msg_equals(self.value, new_value):
            return

        self._value = new_value
        self._value_changed_callback()

    def _send_confirmation(self, warning: str):
        if self._value is not None:
            self._send_confirmation_with_value(warning, self._value)
        else:
            self._send_confirmation_without_value(warning)

    def _send_confirmation_with_value(self, warning: str, value: T):
        buffer = self._value_encoder(value)
        fingerprint, payload = buffer[:8], buffer[8:]
        self._send_confirmation_with(warning, fingerprint, payload)

    def _send_confirmation_without_value(self, warning: str):
        fingerprint = self._value_encoder(self._value_type())[:8]
        self._send_confirmation_with(warning, fingerprint)

    def _send_confirmation_with(self, warning: str, fingerprint: bytes, payload: bytes = b""):
        ack = roc_ack()
        ack.message = warning
        ack.fingerprint = fingerprint
        ack.value = payload
        ack.len = len(ack.value)

        self._confirmation_channel << ack

    @property
    def _value_encoder(self):
        return get_message_encoder(self._value_type)
