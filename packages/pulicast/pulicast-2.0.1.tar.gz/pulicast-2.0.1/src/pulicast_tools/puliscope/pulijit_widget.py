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
from PySide2 import QtCore, QtGui
from PySide2.QtGui import QDoubleValidator
from PySide2.QtWidgets import QFormLayout, QLineEdit, QHBoxLayout, QLabel, QWidget, QPushButton

from pulicast.node import Node
from pulicast.address import Address
from pulicast.channel import Channel
from pulicast.discovery.channel_view import ChannelView
from pulicast.discovery.channel_discoverer import ChannelDiscoverer
from pulicast.discovery.node_discoverer import NodeDiscoverer
from pulicast_tools.puliscope.pulijit.histogram import JitterHistogramWidget


class PulijitWidget(QWidget):
    def __init__(self, node: Node, node_discoverer: NodeDiscoverer, parent=None):
        # node und node_discoverer sind nicht mehr benötigt
        # Referenz auf channel-discoverer übergeben
        super().__init__(parent=parent)
        self._node = node
        self._node_discoverer = node_discoverer
        self._channel_discoverer = ChannelDiscoverer(self._node_discoverer)

        # The main layout
        self.layout = QHBoxLayout(self)

        # Left: Histogram, right: fillable form.
        self.form = QWidget(self)
        self.form_layout = QFormLayout(self.form)
        self._histogram = JitterHistogramWidget()
        self.layout.addWidget(self._histogram)
        self._histogram.reset_data()

        # Upper part of the form:
        # * Channel selection via text input
        # * Expected period: Places a vertical line on the desired frequency
        # * Minimal, maximum period: Only period within this interval are plotted
        self.editor_channel_name = QLineEdit()
        self.editor_channel_name.setPlaceholderText("<Enter a channel>")
        self.editor_channel_name.returnPressed.connect(lambda : self.subscribe_by_name(self.editor_channel_name.text()))
        self.editor_exp_period = QLineEdit("0.001")
        self.editor_min_period = QLineEdit("0")
        self.editor_max_period = QLineEdit("0.1")
        self.editor_exp_period.returnPressed.connect(self.set_expected_period)
        self.editor_min_period.returnPressed.connect(self.set_histogram_clip_range)
        self.editor_max_period.returnPressed.connect(self.set_histogram_clip_range)
        # QDoubleValidator allows only numbers with either zero or three decimals! What's going on?
        #double_validator = QDoubleValidator(parent=self)
        #self.editor_exp_period.setValidator(double_validator)
        #self.editor_min_period.setValidator(double_validator)
        #self.editor_max_period.setValidator(double_validator)
        self.form_layout.addRow(QLabel("channel"), self.editor_channel_name)
        self.form_layout.addRow(QLabel("expected period (ms)"), self.editor_exp_period)
        self.form_layout.addRow(QLabel("min period (ms)"), self.editor_min_period)
        self.form_layout.addRow(QLabel("max period (ms)"), self.editor_max_period)
        self.button_pause_anim = QPushButton("Pause/Unpause animation")
        self.button_pause_anim.clicked.connect(self.toggle_pause)
        self.label_pause_anim = QLabel("Unpaused")
        self.form_layout.addRow(self.button_pause_anim, self.label_pause_anim)
        self.label_mean_period = QLabel()
        self.label_var_period = QLabel()
        self.form_layout.addRow(QLabel("Mean period"), self.label_mean_period)
        self.form_layout.addRow(QLabel("Period variance"), self.label_var_period)
        self.layout.addWidget(self.form)
        self.update_freqs()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update_widget)
        self._timer_period_ms = 250
        self._timer.start(self._timer_period_ms)

    def update_widget(self):
        self._histogram.repaint_histogram()
        mean, variance = self._histogram._histogram.period_mean_and_variance
        if mean is not None and variance is not None:
            self.label_mean_period.setText("{:.2f}ms".format(mean*1e3))
            self.label_var_period.setText("{:.2f}ms²".format(variance*1e6))
        QtGui.QApplication.processEvents()

    def toggle_pause(self):
        if self._timer.isActive():
            self._timer.stop()
            self.label_pause_anim.setText("Paused")
        else:
            self._timer.start(self._timer_period_ms)
            self.label_pause_anim.setText("Unpaused")

    def update_freqs(self):
        self.set_expected_period()
        self.set_histogram_clip_range()

    def set_expected_period(self):
        try:
            self._histogram.set_expected_period(float(self.editor_exp_period.text()))
        except Exception as e:
            print("Pulijit ERROR: Could not apply desired expected periods.")
            print("Caught exception: ", e)

    def set_histogram_clip_range(self):
        try:
            self._histogram.set_clip_range(
                float(self.editor_min_period.text()),
                float(self.editor_max_period.text()),)
        except Exception as e:
            print("Pulijit ERROR: Could not apply desired min/max periods.")
            print("Caught exception: ", e)

    def subscribe_by_name(self, channel_name: str):
        try:
            channel = self._channel_discoverer[channel_name]
        except Exception:
            print("Could not find channel \"{channel_name}\".")
            return
        return self.subscribe(self._channel_discoverer[channel_name])

    @QtCore.Slot(ChannelView)
    def subscribe(self, channel_view: ChannelView):
        self._node[channel_view.name].subscribe(self.new_data_cb)
        self._histogram.reset_data()
        self.editor_channel_name.setText(channel_view.name)
        self.label_mean_period.setText("-")
        self.label_var_period.setText("-")

    def new_data_cb(self, msg):
        """new_data_cb Is called when a new message arrives on the configured channel.
        """
        # Method 1: Compute jitter based on message timestamps
        if not hasattr(msg, "ts"):
            print("Pulijit ERROR: Incoming message doesn't have a field named 'ts'.")
            return

        self._histogram.append_timestamp(float(msg.ts) * 1e-9)

        # Method 2: Compute jitter based on time of arrival
        #self._histogram.append_timestamp(float(time.time()))
