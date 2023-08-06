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
import struct
from typing import List, Optional, Type, Any, Dict
from unittest.mock import Mock

import pytest
import pulicast_messages

from pulicast import Address
from tests.utils.mock_subscriptions import assert_called_once_with_message, setup_mock_subscription, reset_all_mocks
from tests.utils.mock_transports import make_channel_with_mock_transport


def test_publish():
    # GIVEN
    ch, transport = make_channel_with_mock_transport()
    channel_sender = ch._sequence_numbered_sender._channel_sender

    # WHEN
    ch << "Hello World"

    # THEN
    assert len(channel_sender.sent_packets) == 1
    assert pulicast_messages.string_msg.decode(channel_sender.sent_packets[0][4:]).value == "Hello World"
    assert ch._sequence_numbered_sender.sequence_number == 1


def test_initialization():
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    # THEN
    assert ch.name == "channel_name"
    assert not ch.is_subscribed
    assert not ch.is_published
    assert ch.publishing_period == 0
    assert ch._sequence_numbered_sender.sequence_number == 0


def test_subscribe_as_notification_only():
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    mock_handler = Mock()
    # NOTE: we can not subscribe directly to the mock because the mock object has no type annotations
    ch.subscribe(lambda: mock_handler())

    # WHEN
    ch << "Hello World"

    # THEN
    mock_handler.assert_called_once_with()


PRIMITIVE_TYPES = [int, str, float, bool]
PRIMITIVE_VALUES: Dict[Type, List[Any]] = {
    int: [-5, 0, 10],
    str: ["", "hello world", "[]123/.,m"],
    float: [0.0, -0.5, 7.7],
    bool: [True, False]
}


@pytest.mark.parametrize("msg_type", PRIMITIVE_TYPES)
@pytest.mark.parametrize("lead_type_annotation", [None, int])
@pytest.mark.parametrize("source_type_annotation", [None, Address])
@pytest.mark.parametrize("as_method", [True, False])
def test_publish_and_subscribe_to_primitives(msg_type: Type, lead_type_annotation: Optional[int], source_type_annotation: Optional[Address], as_method: bool):
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    current_mock = setup_mock_subscription(msg_type, lead_type_annotation, source_type_annotation, as_method, ch)
    other_mocks: List[Mock] = [setup_mock_subscription(msg_t, lead_type_annotation, source_type_annotation, as_method, ch) for msg_t in PRIMITIVE_TYPES if msg_t != msg_type]

    for test_message in PRIMITIVE_VALUES[msg_type]:
        # WHEN
        reset_all_mocks(other_mocks + [current_mock])
        ch << test_message

        # THEN
        assert_called_once_with_message(current_mock, test_message)
        for mock in other_mocks:
            mock.assert_not_called()


@pytest.mark.parametrize("lead_type_annotation", [None, int])
@pytest.mark.parametrize("source_type_annotation", [None, Address])
@pytest.mark.parametrize("as_method", [True, False])
def test_subscribe_to_any_type(lead_type_annotation: Optional[int], source_type_annotation: Optional[Address], as_method: bool):
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    any_cb = setup_mock_subscription(Any, lead_type_annotation, source_type_annotation, as_method, ch)
    optional_any_cb = setup_mock_subscription(Optional[Any], lead_type_annotation, source_type_annotation, as_method, ch)
    unannotated_cb = setup_mock_subscription(None, lead_type_annotation, source_type_annotation, as_method, ch)

    # WHEN -- publishing something undecodable
    ch.publish(b"asdlkjzhxlkjh")

    # THEN
    any_cb.assert_not_called()
    assert_called_once_with_message(optional_any_cb, None)
    unannotated_cb.assert_not_called()

    # WHEN -- publishing a message
    reset_all_mocks([any_cb, optional_any_cb, unannotated_cb])
    ch << "Hello World"

    #THEN
    assert_called_once_with_message(any_cb, "Hello World")
    assert_called_once_with_message(optional_any_cb, "Hello World")
    assert_called_once_with_message(unannotated_cb, "Hello World")


@pytest.mark.parametrize("lead_type_annotation", [None, int])
@pytest.mark.parametrize("source_type_annotation", [None, Address])
@pytest.mark.parametrize("as_method", [True, False])
def test_subscribe_to_zcm_type(lead_type_annotation: Optional[int], source_type_annotation: Optional[Address], as_method: bool):
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    logmessage_cb = setup_mock_subscription(str, lead_type_annotation, source_type_annotation, as_method, ch)
    optional_logmessage_cb = setup_mock_subscription(Optional[str], lead_type_annotation, source_type_annotation, as_method, ch)

    # WHEN
    ch << "Hello World"

    # THEN
    logmessage_cb.assert_called_once()
    assert logmessage_cb.call_args[0][0] == "Hello World"

    optional_logmessage_cb.assert_called_once()
    assert optional_logmessage_cb.call_args[0][0] == "Hello World"

    # WHEN
    reset_all_mocks([logmessage_cb, optional_logmessage_cb])
    ch << pulicast_messages.pulicast_node()

    # THEN
    logmessage_cb.assert_not_called()
    assert_called_once_with_message(optional_logmessage_cb, None)


def test_is_subscribed():
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    # WHEN
    ch.subscribe(lambda: None)

    # THEN
    assert ch.is_subscribed


def test_is_published():
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    # WHEN
    ch << ""

    # THEN
    assert ch.is_published


def test_wrong_message_type_annotation():
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    def handler(msg: dict):
        print(msg)

    # THEN
    with pytest.raises(ValueError, match="Unsupported message type*"):

        # WHEN
        ch.subscribe(handler)


def test_wrong_lead_type_annotation():
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    def handler(msg, lead: float):
        print(msg)

    # THEN
    with pytest.raises(ValueError, match="The lead argument must be an integer*"):

        # WHEN
        ch.subscribe(handler)


def test_wrong_source_type_annotation():
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    def handler(msg, source: int):
        print(msg)

    # THEN
    with pytest.raises(ValueError, match="The source argument must be a SocketID*"):

        # WHEN
        ch.subscribe(handler)


@pytest.mark.parametrize("as_method", [True, False])
def test_ordered_subscription(as_method: bool):
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    handler = setup_mock_subscription(bytes, int, Address, as_method, ch, ordered=True)

    packets_ordered = [bytearray(struct.pack("!I", seq_no)) + bytearray(str(seq_no).encode("utf8")) for seq_no in (1, 2, 3, 4, 5)]

    packets_unordered = [bytearray(struct.pack("!I", seq_no)) + bytearray(str(seq_no).encode("utf8")) for seq_no in (1, 2, 4, 3, 5)]

    # WHEN
    for packet in packets_ordered:
        transport.simulate_packet(packet, Address(0, 0), ch.name)
    for packet in packets_unordered:
        transport.simulate_packet(packet, Address(0, 1), ch.name)

    # THEN
    received_messages = [call[0][0] for call in handler.call_args_list]
    received_sources = [call[1]['source'] for call in handler.call_args_list]

    expected_messages = [b"1", b"2", b"3", b"4", b"5", b"1", b"2", b"4", b"5"]
    expected_sources = [Address(0, 0), Address(0, 0), Address(0, 0), Address(0, 0), Address(0, 0),
                        Address(0, 1), Address(0, 1), Address(0, 1), Address(0, 1)]

    assert received_sources == expected_sources
    assert received_messages == expected_messages


@pytest.mark.parametrize("as_method", [True, False])
def test_ordered_subscription_simple(as_method: bool):
    """Just ensures that some messages are dropped when they arrive out of order."""
    # GIVEN
    ch, transport = make_channel_with_mock_transport("channel_name")

    handler = Mock()

    def handler_wrapper():
        handler()

    ch.subscribe_ordered(handler_wrapper)

    # Only the first packet should arrive
    packets = [bytearray(struct.pack("!I", seq_no)) + b"payload" for seq_no in (5, 1, 2, 3, 4)]

    # WHEN
    for packet in packets:
        transport.simulate_packet(packet, Address(123, 123), ch.name)

    # THEN
    assert handler.call_count == 1
