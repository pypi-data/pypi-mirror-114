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

import pytest

from pulicast_tools.puliconf.setting_view import zcm_msg_equals
from pulicast_tools.puliconf.utils import convert_toml_value_to_puli_serializable, convert_puli_serializable_to_toml_value
from tests.test_puliconf import test_channel_msg, test_node_msg


@pytest.mark.parametrize("msg", [0, 0., 1, 1., -1, "Test", test_channel_msg, test_node_msg])
def test_zcm_dict_conversion(msg):
    assert zcm_msg_equals(msg, convert_toml_value_to_puli_serializable(convert_puli_serializable_to_toml_value(msg)))