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
import warnings
from threading import Thread
from typing import Optional, Callable

import pulicast
from pulicast.node import Node
from pulicast.transport.plain_socket_transport import PlainSocketTransport


class ThreadedNode(Node):
    """
    A pulicast node that uses the socket API directly and separate threads for timing and dispatch of subscription
    handlers.


    .. warning::
        The intention of this class is to enhance backwards compatibility.
        Since it uses multiple threads, there could be race conditions which right now ar totally ignored by the
        implementation.

    .. warning::
        The ThreadedNode must be started by either calling `run()` (blocking)
        or `start()` (nonblocking in a new thread).

    """
    def __init__(self, name: str, port: int = pulicast.DEFAULT_PORT, ttl: int = 0, heartbeat_period=0.1,
                 interface_address: Optional[str] = None, default_namespace: str = "/"):
        """
        :param name: The name with which the node will be announced in the pulicast network. It is possible to announce
        multiple nodes with the same name but it is advised, that those nodes should behave in the same way (originate
        from the same executable) to avoid confusion.
        :param port: The port on which to open sockets for publishing and subscribing to messages.
        :param ttl: The `time to live <https://en.wikipedia.org/wiki/Time_to_live>`_ for messages being sent.
        Set to 0 to keep the traffic on the local machine.
        :param heartbeat_period: The period in seconds with which the node should announce itself.
        :param interface_address: A network interface to bind to when sending and receiving multicast messages.
        If set to ``"0.0.0.0"`` (the default) messages will be sent and received on all network interfaces.
        Note: if you pass an invalid interface here, an exception will be thrown when making the first subscription,
        not when the node is created.
        :param default_namespace: The namespace, in which the channels are created by default.
            The default is the root namespace '/'.
        """
        self._transport = PlainSocketTransport(port, ttl, interface_address)
        super().__init__(name, default_namespace, heartbeat_period, self._transport)
        self._run_thread: Optional[Thread] = None
        self._is_running: bool = False
        self._last_announcement_time: Optional[float] = None

    def start(self):
        """
        Start another thread to execute subscription handlers and announce the node until `stop()` is called.
        """
        if self._is_running:
            warnings.warn("Pulicast node already running!")
        else:
            if self._run_thread and self._run_thread.is_alive():
                self._run_thread.join()
            self._run_thread = Thread(target=self.run, daemon=True)
            self._run_thread.start()

    def run(self):
        """
        Executes subscription handlers and announces the node. Blocks until `stop()` is called.
        """
        self._is_running = True
        while self._is_running:
            self._transport.handle_some(self.heartbeat_period)
            self._announce_node_if_due()

    def stop(self):
        """
        Stops a running node no matter whether it has been started by `run()` or by `start()`.

        Will wait for running threads to terminate. Note, that a stopped node can not be started again!
        """
        if self._is_running:
            self._is_running = False
            if self._run_thread:
                self._run_thread.join()
            self._transport.stop()
        else:
            warnings.warn("Pulicast node can not be stopped because it is not yet running!")

    def run_one(self):
        """
        Executes subscription handlers for packets in the input queue. If there are no packets, it waits (and blocks)
        for at least the time of the announcement period. Also announces the node if an announcement is due.
        """
        self._announce_node_if_due()
        self.receiver.handle_some(self.heartbeat_period)
        self._announce_node_if_due()

    def poll(self):
        """
        Executes subscription handlers for available packets. Also announces the node if it is due. Will not block.
        """
        self.receiver.handle_some(0)
        self._announce_node_if_due()

    def pause_subscriptions(self):
        """
        Will pause the subscription of all incoming messages.
        Note that there will be message loss, when the subscriptions are paused for long enough that the os-level
        receive buffers run full.
        """
        self._transport.subscriptions_paused = True

    def resume_subscriptions(self):
        """
        Resumes previously paused subscriptions.
        """
        self._transport.subscriptions_paused = False

    def _announce_node_if_due(self):
        if self._last_announcement_time is None or time.time() - self._last_announcement_time > self.heartbeat_period:
            self.announce_node()

    def announce_node(self):
        super().announce_node()
        self._last_announcement_time = time.time()

    def run_later(self, delay: float, callback: Callable[[], None]):
        """
        Runs a function after some delay using a new thread that first sleeps and then executes the function.

        Note: There are no accuracy guarantees for callbacks scheduled this way.

        :param delay: The time in seconds to wait before executing the callback.
        :param callback: The function to execute.
        """
        def wait_and_call_callback():
            time.sleep(delay)
            callback()
        Thread(target=wait_and_call_callback, daemon=True).start()




