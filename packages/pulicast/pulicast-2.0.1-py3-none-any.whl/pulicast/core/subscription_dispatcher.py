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
import weakref
from typing import Callable, List, Optional

from pulicast import Address

SubscriptionCallback = Callable[[bytearray, Address, int], None]


class SubscriptionHandle:
    """
    A subscriptions lifetime is tied to its subscription handle. When the subscription handle is deleted or its
    `unsubscribe` function is called, then the subscription is waived.
    """
    def __init__(self, subscription_callback: SubscriptionCallback, dispatcher: 'SubscriptionDispatcher'):
        self._finalizer = weakref.finalize(self, dispatcher._subscriptions.remove, subscription_callback)

    def unsubscribe(self):
        self._finalizer()


class SubscriptionDispatcher:
    def __init__(self):
        self._subscriptions: List[SubscriptionCallback] = []

    def dispatch(self, packet: bytearray, source: Address, lead: int):
        for callback in self._subscriptions:
            callback(packet, source, lead)

    def subscribe(self, callback: SubscriptionCallback, with_handle: bool) -> Optional[SubscriptionHandle]:
        self._subscriptions.append(callback)
        if with_handle:
            return SubscriptionHandle(callback, self)
        else:
            return None
