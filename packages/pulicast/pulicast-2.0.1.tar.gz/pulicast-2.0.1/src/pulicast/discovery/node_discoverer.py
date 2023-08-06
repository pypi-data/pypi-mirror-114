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
import time

from pulicast_messages import pulicast_node

from pulicast.discovery.node_view import NodeView
from pulicast.core.utils.observable_dict import ObservableDict
from pulicast.node import Node
from pulicast.address import Address


class NodeDiscoverer(ObservableDict):
    """
    The NodeDiscoverer is an :class:`.ObservableMap` that will contain a :class:`.NodeView` for every currently live
    node in the pulicast network. Connecting an disconnection of remote nodes can be observed by registering callbacks
    to the :class:`.ObservableMap`.
    """

    def __init__(self, node: Node):
        super().__init__()
        self._node = node
        node['__nodes'].subscribe_ordered(self._on_node_message)

    def _on_node_message(self, node_info: pulicast_node, source: Address):
        session_id = node_info.session_id

        if session_id in self:
            self[session_id].update(node_info, source)
        else:
            self[session_id] = NodeView(node_info, source)

            def _check_if_node_dead():
                if self[session_id].is_dead:
                    del self[session_id]
                else:
                    check_again_after = max(0, (self[session_id].deadline - time.time()))
                    self._node.run_later(check_again_after, _check_if_node_dead)

            _check_if_node_dead()

