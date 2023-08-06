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
import math
import time

import trio

from pulicast import TrioNode
from pulicast_tools.puliconf.setting import Setting, accept_at_least, accept_only, accept_range


def compute_function(function: str, amplitude: float, offset: float, freq: float, x: float):
    if function == "sin":
        return math.sin(x * freq + offset) * amplitude

    if function == "cos":
        return math.cos(x * freq + offset) * amplitude;

    if function == "saw":
        return ((x * freq + offset) - math.floor(x * freq + offset)) * amplitude;
    return 0


async def main():
    async with trio.open_nursery() as nursery:
        node = TrioNode("python_function_generator", nursery)

        ns = node.make_namespace("pyfunc")

        function_name = Setting("function_name", ns, "sin", validate_roc=accept_only("sin", "cos", "saw"))
        sampling_period = Setting("sampling_period", ns, 0.1, validate_roc=accept_range(0.01, 1.0))
        amplitude = Setting("amplitude", ns, 1.0, validate_roc=accept_at_least(0))
        offset = Setting("offset", ns, 0.0)
        freq = Setting("freq", ns, 1, validate_roc=accept_at_least(0.0))

        x = trio.current_time()
        while True:
            ns["generated_signal"] << compute_function(function_name.value, amplitude.value, offset.value, freq.value, x)
            x += sampling_period.value
            await trio.sleep_until(x)


if __name__ == '__main__':
    trio.run(main)
