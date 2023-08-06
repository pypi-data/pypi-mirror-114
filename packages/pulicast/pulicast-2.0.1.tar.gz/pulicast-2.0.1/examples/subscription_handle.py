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
from pulicast import ThreadedNode

node = ThreadedNode("test")

channel = node["asdf"]

handle = channel.subscribe(callback=lambda x: print(x), with_handle=True)
print(channel.is_subscribed)  # True: since we hold the handle to the subscription

l = [handle]  # store handle in list
del handle  # delete the handle reference but there is still one reference in the list
print(channel.is_subscribed)  # True: since there is still the handle reference in the list

del l  # delete the list and therefore the last reference to the handle
print(channel.is_subscribed)  # False: the handle has been deleted by now
