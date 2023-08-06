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
import numpy as np
import pyqtgraph as pg
from PySide2 import QtCore

class RingBuffer:
    """RingBuffer is an implementation of a circular buffer.
    """

    def __init__(self, capacity: int):
        """
        Parameters
        ----------
        capacity : int
            The ringbuffer's maximum size
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")
        self._arr = np.zeros(capacity)
        self._idx = 0
        self._is_full = False

    def append(self, value: float):
        """append appends a value to the ring buffer. If the buffer is full,
        the values stored in the buffer's front are overwritten.

        Parameters
        ----------
        value : float
            The value to be appended to the ring buffer
        """
        self._arr[self._idx] = value
        self._idx = (self._idx + 1) % self.maxlen
        self._is_full = self._is_full or self._idx == 0

    def reset(self):
        """reset sets the index to zero, effectively emptying the buffer.
        """
        self._idx = 0
        self._is_full = False

    @property
    def lastidx(self):
        """lastidx returns the index of the most recent value appended to the buffer.
        """
        return (self._idx - 1) % self.maxlen

    @property
    def lastval(self):
        """lastval returns the most recent value appended to the buffer.
        """
        return self._arr[self.lastidx]

    @property
    def maxlen(self):
        """maxlen returns the buffer's maximum capacity.
        """
        return self._arr.shape[0]

    @property
    def data(self):
        """data returns the data stored in the buffer.
        """
        return self._arr[:len(self)]

    @property
    def data_unrolled(self):
        """data_unrolled returns the data stored in the buffer, realigned such that the most recently
        appended item is in the last cell.
        """
        if self._is_full:
            return np.roll(self.data, -(self.lastidx + 1))
        else:
            return self.data

    def __len__(self):
        """__len__ returns the buffer size. Returns the maximum capacity if the buffer has been
        filled completely at least once.
        """
        return self._idx if not self._is_full else self.maxlen


class JitterHistogram:
    """JitterHistogram provides a convenient interface for a numpy histogram specifically meant to
    show jitter (= intervals between consecutively arriving timestamped messages).
    """

    def __init__(self, buffer_size: int = 1000, num_bins: int = 100, min_period: float = 0, max_period: float = 0.1):
        """
        Parameters
        ----------
        buffer_size : int
            Determines how many timestamps can be stored at the same time.
        num_bins : int
            Number of histogram bins.
        min_period : float
            Minimum period considered in the histogram.
        max_period : float
            Maximum period considered in the histogram.
        """
        self._timestamps = RingBuffer(capacity=buffer_size)
        self._hist_bins = np.linspace(min_period, max_period, num_bins)

    def set_clip_range(self, min_period: float, max_period: float):
        """set_clip_range sets the minimum and maximum periods considered by the histogram.
        Values falling outside of this range are neglected.
        """
        if min_period >= max_period:
            raise ValueError("minimal period has to be strictly smaller than maximum period!")
        self._hist_bins = np.linspace(min_period, max_period, len(self._hist_bins))

    @property
    def histogram_values(self):
        """histogram_values computes and returns a numpy.histogram showing the
        distribution of periods between consecutive timestamps. Periods
        falling outside the clip range are neglected.
        """
        periods = self.periods
        min_period, max_period = self.clip_range
        periods = periods[(min_period < periods) & (periods <= max_period)]
        return np.histogram(periods, bins=self._hist_bins)

    @property
    def clip_range(self):
        """clip_range returns a tuple containing the minimum period as the first
        element and the maximum period as the second element. Values outside of
        this range are not used in the histogram computation.
        """
        return self._hist_bins[0], self._hist_bins[-1]

    @property
    def periods(self):
        """periods returns a numpy.ndarray containing the periods between the
        stored timestamps. The most recent period is located in the last buffer cell.
        """
        return np.diff(self._timestamps.data_unrolled)

    @property
    def period_mean_and_variance(self):
        """period_mean_and_variance returns a (mean, variance) tuple of the periods between
        the stored consecutive timestamps. If no timestamps are stored, a (None, None) tuple
        is returned.
        """
        if len(self._timestamps) > 1:
            periods = self.periods
            return np.mean(periods), np.var(periods)
        return None, None

    def reset_data(self):
        """reset_data Empties the ring-buffers
        """
        self._timestamps.reset()

    def append_timestamp(self, timestamp: float):
        """append_timestamp appends a new timestamp to the internal ring buffer.
        """
        self._timestamps.append(timestamp)


class JitterHistogramWidget(pg.PlotWidget):
    """JitterHistogramWidget is a pyqtgraph widget for displaying a JitterHistogram object.
    """

    def __init__(self, parent=None):
        """
        Parameters
        ----------
        parent
            The QWidgt's parent object
        """
        super().__init__(parent, title="Message Period Histogram")
        self.setLabel('bottom', 'Message Period', unit='ms')
        self.setLabel('left', 'Occurances')

        # Create some pens for drawing
        pen_red_dashed = pg.mkPen(color='r', width=2, style=QtCore.Qt.DashLine)
        color_blue = pg.mkColor('b')

        self._histogram = JitterHistogram()
        y_vals, x_vals = self._histogram.histogram_values
        self._histogram_plt = pg.PlotCurveItem(x_vals, y_vals, stepMode=True, fillLevel=0, brush=color_blue)
        self.addItem(self._histogram_plt)

        # Draw predicted/desired mean period
        self._expected_mean_vline = pg.InfiniteLine(0.001, pen=pen_red_dashed)
        self.addItem(self._expected_mean_vline)

    def set_expected_period(self, expected_period: float):
        """set_expected_period sets the position of the vertical line indicating the
        expected period.

        Parameters
        ----------
        expected_period : float
            The position of the vertical line indicating the expected period
        """
        self._expected_mean_vline.setValue(expected_period)

    def set_clip_range(self, min_shown_period: float, max_shown_period: float):
        """set_clip_range sets the minimum and maximum periods considered by the histogram.
        Values falling outside of this range are neglected.

        Parameters
        ----------
        min_shown_period : float
            The histogram's left border value
        max_shown_period : float
            The histogram's right border value
        """
        self._histogram.set_clip_range(min_shown_period, max_shown_period)

    def reset_data(self):
        """reset_data Empties the ring-buffers
        """
        self._histogram.reset_data()

    def append_timestamp(self, timestamp: float):
        """append_timestamp appends a new timestamp to the histogram's buffer.
        
        Parameters
        ----------
        timestamp : float
            The timestamp to be appended
        """
        self._histogram.append_timestamp(timestamp)

    def repaint_histogram(self):
        """repaint_histogram Updates the histogram graph, the period
        marker position and the graph's x/y-ranges.
        """
        # Set histogram and marker
        occurances, periods = self._histogram.histogram_values
        self._histogram_plt.setData(periods, occurances)

        # Set ranges
        self.setXRange(*self._histogram.clip_range)
        max_actual_occurances = occurances.max()
        max_possible_occurances = self._histogram._timestamps.maxlen
        self.setYRange(0, max(max_possible_occurances/2.0, max_actual_occurances))