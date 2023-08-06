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
import pytest
import copy

def hist():
    from pulicast_tools.puliscope.pulijit.histogram import JitterHistogram
    return JitterHistogram()

@pytest.fixture
def histogram():
    return hist()

def get_timestamps_ordered():
    return [1, 2]

def get_timestamps_unordered():
    return [2, 1]

def get_timestamps_duplicated():
    return [1, 1]

def get_timestamps_alot_ordered(histogram):
    return np.arange(2*histogram._timestamps.maxlen)

def get_timestamps_alot_random(histogram):
    return np.random.random_integers(0, np.iinfo(np.int64).max, 2*histogram._timestamps.maxlen)

@pytest.mark.parametrize("timestamps", [
    get_timestamps_ordered(),
    get_timestamps_unordered(),
    get_timestamps_duplicated(),
    get_timestamps_alot_ordered(hist()),
    get_timestamps_alot_random(hist())])
def test_append_timestamp(histogram, timestamps):
    ring_buffer_iter = 0
    for i in range(len(timestamps)):
        ts = timestamps[i]
        histogram_before_add = copy.deepcopy(histogram)
        histogram.append_timestamp(ts)

        # Case: Histogram is empty
        # Outcome: With only one timestamp available, time-intervals can't be
        #   computed. Thus the histogram is all zeros.
        if i == 0:
            assert (histogram.histogram_values[0] == 0).all()
            continue

        # Case: New timestamp is in the past.
        # Outcome: Nothing changed. Timestamp is rejected.
        if ts < histogram._timestamps.lastval:
            assert (histogram.histogram_values[0] == histogram_before_add.histogram_values[0]).all()
            assert (histogram.histogram_values[1] == histogram_before_add.histogram_values[1]).all()
            continue
    
        # New timestamp is accepted
        time_interval = ts - histogram_before_add._timestamps.lastval

        # Case: Time-interval is outside of clip range
        # Outcome: time-interval is neglected
        print(histogram.clip_range)
        if histogram.clip_range[0] >= time_interval or time_interval > histogram.clip_range[1]:
            assert (histogram.histogram_values[0] == histogram_before_add.histogram_values[0]).all()
            assert (histogram.histogram_values[1] == histogram_before_add.histogram_values[1]).all()
            continue

        # Case: Time-interval is accepted
        # Outcome: Timestamp is stored, time-interval is sorted into histogram values
        bin_idx = np.digitize(time_interval, histogram_before_add._hist_bins)
        occurances_new = histogram.histogram_values[0]
        occurances_old = histogram_before_add.histogram_values[0]
        assert occurances_new[bin_idx] == occurances_old[bin_idx] + 1
        assert histogram._timestamps.lastval == ts
        

@pytest.fixture(params=[
    get_timestamps_ordered(),
    get_timestamps_unordered(),
    get_timestamps_duplicated(),
    get_timestamps_alot_ordered(hist()),
    get_timestamps_alot_random(hist())])
def histogram_warmstarted(histogram, request):
    timestamps = request.param
    for ts in timestamps:
        histogram.append_timestamp(ts)
    return histogram

@pytest.mark.parametrize("min_period", [1.0, 3.0])
@pytest.mark.parametrize("max_period", [3.0, 1.0])
def test_set_clip_range(histogram, min_period, max_period):
    if min_period >= max_period:
        with pytest.raises(Exception):
            assert histogram.set_clip_range(min_period, max_period)
    else:
        histogram.set_clip_range(min_period, max_period)
        assert histogram.clip_range == (min_period, max_period)

def test_reset_data(histogram, histogram_warmstarted):
    histogram_warmstarted.reset_data()
    assert (histogram.histogram_values[0] == histogram_warmstarted.histogram_values[0]).all()
    assert (histogram.histogram_values[1] == histogram_warmstarted.histogram_values[1]).all()
    

def test_period_mean_and_variance(histogram_warmstarted):
    time_intervals = np.diff(histogram_warmstarted._timestamps.data)
    mean = np.mean(time_intervals)
    var = np.var(time_intervals)
    assert histogram_warmstarted.period_mean_and_variance == (mean, var)
    histogram_warmstarted.reset_data()
    assert histogram_warmstarted.period_mean_and_variance == (None, None)