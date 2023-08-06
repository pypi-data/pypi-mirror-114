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
import inspect
import logging
import sys
import typing
from typing import Optional, Any, Callable, Type

from pulicast.address import Address
from pulicast.core.lead_extractor import ALL_MESSAGES_LEAD_VALUE, ORDERED_MESSAGE_LEAD_VALUE, LeadExtractor
from pulicast.core.sequence_numbered_sender import SequenceNumberedSender
from pulicast.core.subscription_dispatcher import SubscriptionDispatcher, SubscriptionHandle
from pulicast.core.transport import Transport
from pulicast.serialization import get_message_decoder, get_message_encoder

if sys.version_info < (3, 8):
    import pytypes


class Channel:
    """
    The Channel class allows to publish and subscribe to messages on pulicast channels.
    Messages are everything that can be serialized by pulicast. See :mod:`.serialization`
    for an overview of what can be serialized.

    A pulicast channel is identified by its name. There can be any number of subscribers and publishers on a single
    channel as well as any number of different message types delivered via the channel. However the typical usage
    pattern foresees a single publisher and a single message type.


    .. note::
        Channel objects are typically not instantiated directly but rather obtained via a :class:`.Node`
        object to prevent duplicate channel objects for a single pulicast channel and to ensure proper functioning of
        the discovery mechanisms of pulicast.
    """

    def __init__(self, name: str, transport: Transport):
        """
        Warning: not to be called by user code. Channel objects are to be created by a :class:`.ChannelMap`

        Creates a new channel object.

        :param name: The name of the pulicast channel that this channel object is referring to.
        :param transport: The :class:`.Transport` to use with this channel.
        """
        self.publishing_period: float = 0
        self._name: str = name
        self._transport = transport
        self._subscription_dispatcher_instance: SubscriptionDispatcher = None
        self._sequence_numbered_sender = SequenceNumberedSender(transport.make_channel_sender(name))
        self._lead_extractor = LeadExtractor()

        self._most_recent_msg_type: Optional[typing.Type] = None
        self._most_recent_encoder: Optional[typing.Callable[[typing.Any], bytes]] = None

    def publish(self, data: bytes):
        """
        Publishes a number of bytes on the channel.

        It is assumed, that the bytes contain a serialized message but not necessary.

        :param data: The bytes to publish on the channel.
        """
        self._sequence_numbered_sender.send(bytearray(data))

    def publish_message(self, message: Any):
        """
        Publishes a message on the channel by first serializing it and then sending it via the :func:`.publish` function.

        .. note:: The message has to be serializable. See :mod:`.serialization` for details.

        .. note::
            you can also publish a message to a channel via the left shift operator like this::

                >>> my_channel << my_message

        :param message: The message to send.
        """
        if type(message) != self._most_recent_msg_type:
            self._most_recent_msg_type = type(message)
            self._most_recent_encoder = get_message_encoder(self._most_recent_msg_type)
        self.publish(self._most_recent_encoder(message))

    @property
    def name(self):
        return self._name

    def __lshift__(self, message: Any):
        """
        Alternative way to publish a message. See :func:`.publish` for details.

        :param message: The message to publish.
        """
        self.publish_message(message)

    def subscribe(self, callback: Callable, min_lead: int = ALL_MESSAGES_LEAD_VALUE, with_handle: bool = False):
        """
        Registers a callback to be called when a new message arrives on the channel.

        :param callback: The callback to call when a new message arrives.
        The supported callback signatures include

        * ``()`` (empty) -- will be called whenever any packet arrives on the channel (including empty packets).
        * ``(message)``
        * ``(message, source: SocketID)``
        * ``(message, lead: int)``
        * ``(message, source: SocketID, lead: int)``
        * ``(message, lead: int, source: SocketID)``

        The annotation of the message parameter controls what type of message is being dispatched:

        * No annotation or ``typing.Any``: All messages
        * For any other type annotation only messages of that specific type will be dispatched. This works for
            * the primitive types ``int``, ``float``, ``bool`` and ``str`` which are delivered within zcm messages
              called int64_msg, float_msg ...
            * bytes, which disables any decoding and gives access to the raw message bytes
            * Any of the messages registered with pulicast.serialization.register_zcm_package or pulicast.serialization.register_zcm_type

        If one of the above typing annotation is wrapped in a ``typing.Optional`` and a decoding error occurred,
        a ``None`` message is dispatched.

        :param min_lead: The minimum lead that a message has to have. See :doc:`concepts/ordered_delivery` for details.
        :param with_handle: If set to true this function will return a subscription handle that is tied to the
        subscription.
        :raises ValueError: If the callback is wrongly annotated.
        """

        arg_spec = inspect.getfullargspec(callback)
        # methods have self as first argument. We want to ignore that one here
        if len(arg_spec.args) > 0 and arg_spec.args[0] == "self":
            arg_spec.args.pop(0)

        if len(arg_spec.args) > 0:
            message_arg_name = arg_spec.args[0]
            message_argument_type = arg_spec.annotations.get(message_arg_name, Any)

            if _is_optional_type(message_argument_type):
                message_type = _get_wrapped_type_of_optional(message_argument_type)
                ignore_decode_errors = True
            else:
                message_type = message_argument_type
                ignore_decode_errors = False

            try:
                decoder = get_message_decoder(message_type)
            except KeyError:
                raise ValueError(f"Unsupported message type: {message_type}!")

            if "lead" in arg_spec.annotations:
                if arg_spec.annotations["lead"] != int:
                    raise ValueError(f"The lead argument must be an integer, not {arg_spec.annotations['lead']}!")

            if "source" in arg_spec.annotations:
                if arg_spec.annotations["source"] != Address:
                    raise ValueError(f"The source argument must be a SocketID, not {arg_spec.annotations['source']}!")

            consumes_lead = "lead" in arg_spec.args
            consumes_source = "source" in arg_spec.args

            def decoding_cb(message_bytes: bytearray, source: Address, lead: int):
                if lead < min_lead:
                    logging.warning(f"Dropping message on {self.name} since "
                                    f"its lead {lead} is smaller than the minimum lead {min_lead}!")
                    return
                decoded_message = decoder(message_bytes)
                if not ignore_decode_errors and decoded_message is None:
                    logging.info(f"Dropping message on {self.name} since "
                                    f"there was an decoding error!")
                    return
                call_dict = {message_arg_name: decoded_message}
                if consumes_lead:
                    call_dict['lead'] = lead
                if consumes_source:
                    call_dict['source'] = source
                callback(**call_dict)

            return self._subscription_dispatcher.subscribe(decoding_cb, with_handle)
        else:
            def dumb_cb(message_bytes: bytes, source: Address, lead: int):
                if lead < min_lead:
                    return
                callback()
            return self._subscription_dispatcher.subscribe(dumb_cb, with_handle)

    def subscribe_ordered(self, callback: Callable, with_handle: bool = False) -> Optional[SubscriptionHandle]:
        """
        Like :func:`.subscribe` but only delivers messages in order. Messages that arrive out of order are being
        dropped.

        :param callback: The callback to call when a new message arrives. See :func:`.subscribe` for an overview over
        supported signatures.
        :param with_handle: If set to true this function will return a subscription handle that is tied to the
        subscription.

        """
        return self.subscribe(callback, ORDERED_MESSAGE_LEAD_VALUE, with_handle)

    @property
    def is_subscribed(self):
        """
        :return: True if this node has a subscription on the channel.
        """
        return self._subscription_dispatcher_instance is not None and \
               len(self._subscription_dispatcher._subscriptions) > 0

    @property
    def is_published(self):
        """
        :return: True if something has been published on this channel by this node. False otherwise.
        """
        return self._sequence_numbered_sender.sequence_number > 0

    @property
    def _subscription_dispatcher(self):
        if self._subscription_dispatcher_instance is None:
            self._transport.start_receiving_messages_for(self.name, self._on_new_packet)
            self._subscription_dispatcher_instance = SubscriptionDispatcher()
        return self._subscription_dispatcher_instance

    """
    Notifies the channel of a newly arrived packet.

    This would only be called by a library user to simulate the reception of a packet.
    In all other cases this is called by the :class:`.Transport`.

    :param data: The data that has been received.
    :param source: The address of the socket that the packed originated from.
    """
    def _on_new_packet(self, data: bytes, source: Address):
        lead = self._lead_extractor.extract_lead(data, source)
        if lead is not None and self._subscription_dispatcher_instance is not None:
            self._subscription_dispatcher_instance.dispatch(data, source, lead)


def _is_optional_type(t: Type):
    if sys.version_info < (3, 8):
        return pytypes.is_Union(t) and \
            isinstance(None, pytypes.get_Union_params(t)[-1])
    else:
        return typing.get_origin(t) is typing.Union and \
            isinstance(None, typing.get_args(t)[-1])


def _get_wrapped_type_of_optional(t: typing.Union):
    if sys.version_info < (3, 8):
        return pytypes.get_Union_params(t)[0]
    else:
        return typing.get_args(t)[0]
