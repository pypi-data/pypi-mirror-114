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
from io import BytesIO
from typing import Any, Optional, Tuple

import trio
from pulicast_messages import reset_setting_to_default, roc_ack, unset_setting

from pulicast.core.utils.observable_property import ObservableProperty
from pulicast.discovery.node_view import NodeView
from pulicast.node import Node
from pulicast.pulicast_trio import open_subscription
from pulicast.serialization import primitive_message_types, zcm_message_types_by_fingerprint
from pulicast_tools.puliconf.channel_naming_conventions import deduce_roc_channel_from_confirmation_channel, \
    deduce_setting_name_from_confirmation_channel


class SettingView:
    """
    The :class:`.SettingView` provides a view on a distributed setting.

    It allows to set the remote setting and checks whether the view is synchronized or locked.
    When a view is synchronized, it is guaranteed that the remote setting and its view have the same value.
    When a setting is locked, its owning node went offline or there was a collision with another distributed setting
    of the same name. A locked view will ignore any future changes of the distributed setting and will not emmit any
    request of changes any more.
    """
    value = ObservableProperty(None)
    is_synced = ObservableProperty(True)
    is_locked = ObservableProperty(False)

    def __init__(self, channel_name: str, initial_ack: roc_ack, owning_node: NodeView, node: Node):
        """
        Creates a new SettingView.

        :param channel_name: The name of the channel on which the setting advertises its current value.
        :param initial_ack: A initial roc_ack message which is used to initialize the view.
        :param owning_node: The view on the node owning the setting.
        :param node: The pulicast node handle to access the pulicast network.
        """
        super().__init__()
        self._node = node
        self._owning_node = owning_node
        self._roc_channel = node["/" + deduce_roc_channel_from_confirmation_channel(channel_name)]
        self._confirmation_channel = node["/" + channel_name]

        self._message_type = SettingView._extract_message_type_from_ack(initial_ack)

        self._initialization_message = initial_ack.message

        try:
            self.value = self._extract_value_from_ack(initial_ack)
        except ValueError:
            logging.warning(f"{self} got an ack with message type {self._message_type}"
                            f" for which the encoded message could not be parsed!")

    async def set(self, target_value: Optional[Any], num_retries: int = 5, retry_period: float = 0.1) -> Tuple[bool, str]:
        """
        Attempts to set the distributed setting to a new value.

        This will cause the view to go out of sync until confirmation has been received by the remote setting.
        As long as no confirmation has been received, the request of change will be repeated with 10Hz.

        :param target_value: The new value of the setting. If `None`, the setting will be reset
        :param num_retries: Of often to retry setting the value when there is no confirmation.
        :param retry_period: The time to wait before re-sending a request of change in case the remote end does not
        answer (time in seconds).
        :return: A tuple of a bool indicating success and a string with an explanation of the failure reason
        (possibly empty). We only consider setting a success when the distributed setting was set to the target value.
        """
        if self.is_locked:
            return False, "Setting is locked!"
        if not self.is_synced:
            return False, "Setting is not synced!"

        is_reset = type(target_value) == reset_setting_to_default
        if not is_reset and target_value is not None and type(target_value) != self.value_type:
            return False, f"Can only set {self} to values of type {self.value_type} and not of type {type(target_value)}!"

        self.is_synced = False
        async with open_subscription(self._confirmation_channel, message_type=roc_ack, min_lead=1) as conf_messages:
            for _ in range(num_retries):
                self._send_roc(target_value)
                with trio.move_on_after(retry_period):
                    ack = await conf_messages.receive()
                    message_type = SettingView._extract_message_type_from_ack(ack)
                    if self._message_type != message_type:
                        logging.warning(f"{self} is of type {self._message_type} but now sent a message of type "
                                        f"{message_type}! We are ignoring this message.")
                        await trio.sleep(retry_period)

                    new_value = self._extract_value_from_ack(ack)
                    self.is_synced = True
                    self.value = new_value
                    explanation = ack.message
                    was_set_to_target = zcm_msg_equals(target_value, self.value)
                    if not is_reset and not was_set_to_target and explanation == "":
                        explanation = f"New value ({self.value}) is not target value({target_value})!"
                    return is_reset or was_set_to_target, explanation
            return False, "Ran out of retries!"

    async def reset(self):
        """
        Attempts to set the distributed setting to its initial value.

        :return: A tuple of a bool indicating success and a string with an explanation of the failure reason
        (possibly empty). We only consider setting a success when the distributed setting was set to its initial value.
        """
        return await self.set(reset_setting_to_default())

    async def unset(self):
        """
        Attempts to set the distributed setting to a None value.

        :return: A tuple of a bool indicating success and a string with an explanation of the failure reason
        (possibly empty). We only consider setting a success when the distributed setting was set to None.
        """
        return await self.set(None)

    def _send_roc(self, target_value):
        if target_value is None:
            self._roc_channel << unset_setting()
        elif self._message_type in primitive_message_types and not isinstance(target_value, reset_setting_to_default):
            # Note: Since python only deals with long ints, pulicast implicitly packs all ints into a
            # pulicast_messages.int64_msg. This makes the smaller int types non-viable unless we pack the int into the
            # correct message type explicitly as done below.
            roc = self._message_type()
            roc.value = target_value
            self._roc_channel << roc
        else:
            self._roc_channel << target_value

    def _extract_value_from_ack(self, ack: roc_ack) -> Any:
        if ack.len > 0:
            message = self._message_type._decode_one(BytesIO(ack.value))
            if self._message_type in primitive_message_types:
                return message.value
            else:
                return message
        else:
            return None

    @staticmethod
    def _extract_message_type_from_ack(ack: roc_ack):
        return zcm_message_types_by_fingerprint[ack.fingerprint]

    @property
    def name(self) -> str:
        return deduce_setting_name_from_confirmation_channel(self._confirmation_channel.name)

    def lock(self):
        self.is_locked = True

    @property
    def owning_node(self) -> NodeView:
        return self._owning_node

    @property
    def initialization_message(self) -> str:
        return self._initialization_message

    @property
    def value_type(self) -> type:
        if self._message_type in primitive_message_types:
            return type(self._message_type().value)
        else:
            return self._message_type

    def __str__(self):
        return f"{self.name} at {self.owning_node.name}"


def zcm_msg_equals(lhs: Any, rhs: Any):
    """
    Checks if two values (possibly zcm messages) are equal.

    Note: we need this helper function since zcm messages do not overload the equals operator.

    :param lhs: Left hand side of the comparison.
    :param rhs: Right hand side of the comparison.
    :return: True, if the two values are equal, false if not.
    """
    if isinstance(lhs, (list, tuple)) and isinstance(rhs, (list, tuple)) and len(lhs) == len(rhs):
        return all(zcm_msg_equals(l, r) for l, r in zip(lhs, rhs))
    elif hasattr(lhs, "__slots__") and type(lhs) == type(rhs):
        for field in lhs.__slots__:
            if not zcm_msg_equals(getattr(lhs, field), getattr(rhs, field)):
                return False
        return True
    else:
        return lhs == rhs
