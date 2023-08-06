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
from pulicast_tools.puliscope.pulijit.histogram import RingBuffer

def test_init_zero_capacity():
    with pytest.raises(Exception):
        assert RingBuffer(capacity=0)

@pytest.fixture
def data():
    return np.random.random(200)

@pytest.fixture
def buf():
    return RingBuffer(capacity=5)

def test_fill(buf, data):
    for i in range(buf.maxlen):
        buf.append(data[i])
    assert buf.lastval == data[buf.maxlen-1]
    assert (buf.data == buf._arr).all()
    assert len(buf) == buf.maxlen
    assert buf._idx == 0
    for i in range(buf.maxlen):
        assert buf._arr[i] == data[i]

def test_fill_overwrite(buf, data):
    for i in range(2 * buf.maxlen):
        buf.append(data[i])
    assert buf.lastval == data[2 * buf.maxlen-1]
    assert (buf.data == buf._arr).all()
    assert len(buf) == buf.maxlen
    assert buf._idx == 0
    assert buf._is_full == True
    for i in range(buf.maxlen):
        assert buf._arr[i] == data[buf.maxlen + i]

def test_reset(buf, data):
    for i in range(buf.maxlen):
        buf.append(data[i])
    buf_before_reset = buf
    buf.reset()
    assert buf.maxlen == buf_before_reset.maxlen
    assert (buf.data == buf_before_reset.data).all()
    assert len(buf.data) == 0
    assert len(buf) == 0
    assert buf._idx == 0
    assert buf._is_full == False
    
