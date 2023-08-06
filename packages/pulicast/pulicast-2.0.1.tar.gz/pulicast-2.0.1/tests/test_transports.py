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
from unittest.mock import Mock

import pytest

import numpy as np

from pulicast import ThreadedNode
from pulicast.pulicast_qt import QtNode
from tests.utils.mock_subscriptions import setup_mock_subscription


node_implementations = [ThreadedNode, QtNode]

# TODO(max): any QT test in here are deactivated since they caused segfaults when used with tox

# @pytest.mark.parametrize("sending_node_class", node_implementations)
# @pytest.mark.parametrize("receiving_node_class", node_implementations)
# def test_sending_and_receiving_between_different_nodes(sending_node_class, receiving_node_class):
#     # GIVEN
#     sending_node = sending_node_class("nodeA")
#     receiving_node = receiving_node_class("nodeB")
#
#     sending_node.start()
#     receiving_node.start()
#     mock_cb = setup_mock_subscription(str, None, None, False, receiving_node["test_channel"])
#
#     # WHEN
#     sending_node["test_channel"] << "Hello World"
#
#     # THEN
#     assert mock_cb.called_once_with("Hello World")
#
#     # TEARDOWN
#     sending_node.stop()
#     receiving_node.stop()


def test_run_later_socket():
    # GIVEN
    node = ThreadedNode("test_node")
    t0 = time.time()

    mock_cb = Mock()

    def assert_1_second_elapsed():
        assert np.isclose(time.time() - t0, 1, atol=0.01)
    mock_cb.side_effect = assert_1_second_elapsed

    # WHEN
    node.run_later(1, mock_cb)
    time.sleep(1.1)

    # THEN
    mock_cb.assert_called_once_with()


# TODO(max): use https://pytest-qt.readthedocs.io/en/3.3.0/signals.html here
# TODO(max): here we have a problem because each test starts a new QApplication which QT does not like baybe pytest-qt will solve this for us
# def test_run_later_qt():
#     # GIVEN
#     if QCoreApplication.instance() is None:
#         app = QCoreApplication()
#     else:
#         app = QCoreApplication.instance()
#     node = QtNode("test_node")
#     t0 = time.time()
#
#     mock_cb = Mock()
#
#     def assert_1_second_elapsed_and_exit_app():
#         assert np.isclose(time.time() - t0, 1, atol=0.1)
#         app.exit(0)
#
#     mock_cb.side_effect = assert_1_second_elapsed_and_exit_app
#
#     # WHEN
#     node.run_later(1, mock_cb)
#     app.exec_()
#
#     # THEN
#     mock_cb.assert_called_once_with()
