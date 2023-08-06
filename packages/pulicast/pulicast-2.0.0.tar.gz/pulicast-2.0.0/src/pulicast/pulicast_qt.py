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
from threading import Thread
from typing import Optional, Callable

from PySide2.QtCore import QTimer, QCoreApplication
from PySide2.QtNetwork import QNetworkInterface

import pulicast
from pulicast.node import Node
from pulicast.transport.qt_multicast_transport import QtTransport


class QtNode(Node):
    """A pulicast node that uses the Qt event loop for networking, timing and dispatch of subscription handlers."""

    def __init__(self, name: str, port: int = pulicast.DEFAULT_PORT, ttl: int = 0, heartbeat_period: float = 0.1,
                 interface: Optional[QNetworkInterface] = None, default_namespace: str = "/"):
        """
        Note that the QtNode should be created **after** an instance of a QApplication has been created.

        :param name: The name with which the node will be announced in the pulicast network. It is possible to announce
        multiple nodes with the same name but it is advised, that those nodes should behave in the same way (originate
        from the same executable) to avoid confusion.
        :param port: The port on which to open sockets for publishing and subscribing to messages.
        :param ttl: The `time to live <https://en.wikipedia.org/wiki/Time_to_live>`_ for messages being sent.
        Set to 0 to keep the traffic on the local machine.
        :param heartbeat_period: The period in seconds with which the node should announce itself.
        :param interface: A network interface to bind to when sending and receiving multicast messages.
        If set to ``None`` (the default) messages will be sent and received on all network interfaces.
        Note: if you pass an invalid interface here, an exception will be thrown when making the first subscription,
        not when the node is created.
        :param default_namespace: The namespace, in which the channels are created by default.
            The default is the root namespace '/'.
        """
        self._transport = QtTransport(port, ttl, interface)
        Node.__init__(self, name, default_namespace, heartbeat_period, self._transport)

        # NOTE: we need to put the timer in a member variable, otherwise it goes out of scope and does not trigger.
        self._announcement_timer = announcement_timer = QTimer()
        # NOTE: we need to wrap the call to announce_node in a lambda because otherwise QT does not accept it.
        announcement_timer.timeout.connect(lambda: self.announce_node())
        announcement_timer.start(int(heartbeat_period * 1000))

        self._qt_app: QCoreApplication = None
        self._running_thread: Optional[Thread] = None

    def run_later(self, delay: float, callback: Callable[[], None]):
        """
        Runs a function after some delay using a QTimer.

        Note: There are no accuracy guarantees for callbacks scheduled this way.

        :param delay: The time in seconds to wait before executing the callback.
        :param callback: The function to execute.
        """
        QTimer.singleShot(int(delay*1000), callback)

    def stop(self):
        self._announcement_timer.stop()
        self._transport.stop()



