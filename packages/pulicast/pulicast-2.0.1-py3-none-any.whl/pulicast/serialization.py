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
from typing import Dict, Type, Callable, Any, Union

import pulicast_messages
from pulicast_messages import *


primitive_message_types = (int8_msg, int16_msg, int32_msg, int64_msg, string_msg, boolean_msg, byte_msg, double_msg,
                           float_msg)

primitive_types = (int, float, bool, str)

PrimitiveType = Union[primitive_types]


zcm_message_types_by_fingerprint: Dict[bytes, Type] = dict()


def _raw_bytes_decoder(data: bytes) -> bytes:
    return data


def _make_zcm_static_decoder(type) -> Callable[[bytes], type]:
    def static_decoder(data: bytes):
        try:
            message = type.decode(data)
        except ValueError as e:
            if "Decode error" in e.args:  # We only catch decode errors here. Others will be re-raised
                return None
            else:
                raise e
        return message
    return static_decoder


def _zcm_dynamic_decoder(data: bytearray):
    fingerprint = bytes(data[:8])
    message_type = zcm_message_types_by_fingerprint.get(fingerprint, None)
    if message_type is not None:
        return message_type.decode(data)
    else:
        return None


def _make_primitives_decoder(message_type: PrimitiveType) -> Callable[[bytes], type]:
    def primitive_decoder(data: bytes):
        zcm_message = _zcm_dynamic_decoder(data)
        if zcm_message is None:
            return None
        if not hasattr(zcm_message, "value"):
            return None
        if type(zcm_message.value) != message_type:
            return None
        return zcm_message.value

    return primitive_decoder


def _universal_decoder(data: bytearray) -> Any:
    msg = _zcm_dynamic_decoder(data)

    if isinstance(msg, primitive_message_types):
        return msg.value
    else:
        return msg


_decoders_by_type = {
    bytes: _raw_bytes_decoder,
    Any: _universal_decoder
}


_decoders_by_type.update({
    type: _make_primitives_decoder(type) for type in primitive_types
})


def get_message_decoder(message_type: Type) -> Callable[[bytearray], Any]:
    """
    This assumes message type is either bytes or a zcm message. For message type 'Any' automatic type detection is used.
    """
    return _decoders_by_type[message_type]


def _raw_bytes_encoder(message: bytearray) -> bytes:
    return bytes(message)


def _zcm_encoder(message: Any) -> bytes:
    return message.encode()


def _int_encoder(value: int) -> bytes:
    msg = int64_msg()
    msg.value = value
    return msg.encode()


def _string_encoder(value: str) -> bytes:
    msg = string_msg()
    msg.value = value
    return msg.encode()


def _float_encoder(value: float) -> bytes:
    msg = double_msg()
    msg.value = value
    return msg.encode()


def _bool_encoder(value: bool) -> bytes:
    msg = boolean_msg()
    msg.value = value
    return msg.encode()


def _none_encoder(value: None) -> bytes:
    return b""


_encoders_by_type: Dict[type, Callable[[Any], bytes]] = {
    bytes: _raw_bytes_encoder,
    int: _int_encoder,
    float: _float_encoder,
    bool: _bool_encoder,
    str: _string_encoder,
    type(None): _none_encoder}


def get_message_encoder(message_type: Type) -> Callable[[Any], bytes]:
    # This assumes zcm messages unless its bytes that we deal with
    return _encoders_by_type[message_type]


def is_zcm_type(t):
    return hasattr(t, "decode") and hasattr(t, "encode") and hasattr(t, "_get_packed_fingerprint")


def register_zcm_type(type):
    zcm_message_types_by_fingerprint[type._get_packed_fingerprint()] = type
    _encoders_by_type[type] = _zcm_encoder
    _decoders_by_type[type] = _make_zcm_static_decoder(type)


def register_zcm_package(package):
    types = (type for typename, type in inspect.getmembers(package) if is_zcm_type(type))
    for t in types:
        register_zcm_type(t)

# Note: here we register zcom messages for convenience but only if zcom ist installed.
# This will silently fail if zcom is not installed.
# Note also, that it is important to register zcom BEFORE the pulicast_messages to ensure that the zcom hashes do not
# overwrite the pulicast_messages
try:
    import zcom
    register_zcm_package(zcom)
except:
    pass

register_zcm_package(pulicast_messages)

