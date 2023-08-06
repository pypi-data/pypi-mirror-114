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

from pulicast.discovery.node_view import NodeView
from pulicast.core.utils.observable_set import ObservableSet


class ChannelView:
    """
    The :class:`.ChannelView` describes a channel being used within the pulicast network including its name,
    and :class:`.ObservableSet`s of :class:`.NodeView`s that publish and subscribe on them.
    """
    def __init__(self, name):
        self.name = name
        self.subscribers: ObservableSet[NodeView] = ObservableSet[NodeView]()
        self.publishers: ObservableSet[NodeView] = ObservableSet[NodeView]()
        self.nodes: ObservableSet[NodeView] = ObservableSet[NodeView]()

