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
from typing import Optional, Type, Any
from unittest.mock import Mock

from pulicast.channel import Channel


def reset_all_mocks(mocks):
    for mock in mocks:
        mock.reset_mock()


def setup_mock_subscription(message_type: Optional[Type],
                            lead_type_annotation: Optional[Type],
                            source_type_annotation: Optional[Type],
                            as_method: bool,
                            channel: Channel, ordered=False) -> Mock:
    if as_method:
        return setup_mock_method_subscription(message_type, lead_type_annotation, source_type_annotation, channel, ordered)
    else:
        return setup_mock_function_subscription(message_type, lead_type_annotation, source_type_annotation, channel, ordered)


def setup_mock_function_subscription(message_type: Optional[Type],
                                     lead_type_annotation: Optional[Type],
                                     source_type_annotation: Optional[Type],
                                     channel: Channel, ordered: bool) -> Mock:
    mock_callback = Mock()

    signature_str = make_signature_string(message_type, lead_type_annotation, source_type_annotation)

    if signature_str == "___":
        def handler(msg): mock_callback(msg)

    if signature_str == "__S":
        def handler(msg, source: source_type_annotation): mock_callback(msg, source=source)

    if signature_str == "_L_":
        def handler(msg, lead: lead_type_annotation): mock_callback(msg, lead=lead)

    if signature_str == "_LS":
        def handler(msg, lead: lead_type_annotation, source: source_type_annotation): mock_callback(msg, lead=lead, source=source)

    if signature_str == "M__":
        def handler(msg: message_type): mock_callback(msg)

    if signature_str == "M_S":
        def handler(msg: message_type, source: source_type_annotation): mock_callback(msg, source=source)

    if signature_str == "ML_":
        def handler(msg: message_type, lead: lead_type_annotation): mock_callback(msg, lead=lead)

    if signature_str == "MLS":
        def handler(msg: message_type, lead: lead_type_annotation, source: source_type_annotation): mock_callback(msg, lead=lead,
                                                                                                    source=source)

    # Note: we can not subscribe directly to the mock callback because it does not support type annotations
    if ordered:
        channel.subscribe_ordered(handler)
    else:
        channel.subscribe(handler)
    return mock_callback


def setup_mock_method_subscription(message_type: Optional[Type], lead_type_annotation: Optional[Type], source_type_annotation: Optional[Type], channel: Channel, ordered=False):
    mock_callback = Mock()

    signature_str = make_signature_string(message_type, lead_type_annotation, source_type_annotation)

    if signature_str == "___":
        class MyMockClass:
            def handler(self, msg): mock_callback(msg)

    if signature_str == "__S":
        class MyMockClass:
            def handler(self, msg, source: source_type_annotation): mock_callback(msg, source=source)

    if signature_str == "_L_":
        class MyMockClass:
            def handler(self, msg, lead: lead_type_annotation): mock_callback(msg, lead=lead)

    if signature_str == "_LS":
        class MyMockClass:
            def handler(self, msg, lead: lead_type_annotation, source: source_type_annotation): mock_callback(msg, lead=lead,
                                                                                                    source=source)

    if signature_str == "M__":
        class MyMockClass:
            def handler(self, msg: message_type): mock_callback(msg)

    if signature_str == "M_S":
        class MyMockClass:
            def handler(self, msg: message_type, source: source_type_annotation): mock_callback(msg, source=source)

    if signature_str == "ML_":
        class MyMockClass:
            def handler(self, msg: message_type, lead: lead_type_annotation): mock_callback(msg, lead=lead)

    if signature_str == "MLS":
        class MyMockClass:
            def handler(self, msg: message_type, lead: lead_type_annotation, source: source_type_annotation): mock_callback(msg,
                                                                                                                  lead=lead,
                                                                                                                  source=source)
    mock_object = MyMockClass()
    # Note: we can not subscribe directly to the mock callback because it does not support type annotations
    if ordered:
        channel.subscribe_ordered(mock_object.handler)
    else:
        channel.subscribe(mock_object.handler)
    return mock_callback


def make_signature_string(message_type: Optional[Type], lead_type_annotation: Optional[Type], source_type_annotation: Optional[Type]):
    return ("_" if message_type is None else "M") + \
           ("_" if lead_type_annotation is None else "L") + \
           ("_" if source_type_annotation is None else "S")


def last_received_message(mock_callback: Mock):
    return mock_callback.call_args[0][0]


def assert_called_once_with_message(mock_callback: Mock, target_value: Any, message_attribute: Optional[str] = None):
    mock_callback.assert_called_once()
    message = last_received_message(mock_callback)
    if message_attribute is None:
        assert message == target_value
    else:
        assert getattr(message, message_attribute) == target_value
