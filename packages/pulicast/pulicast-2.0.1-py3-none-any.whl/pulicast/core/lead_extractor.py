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
from typing import Dict

from pulicast import Address
from pulicast.core.utils.extract_from_bytearray import extract_uint32

ORDERED_MESSAGE_LEAD_VALUE = 1
ALL_MESSAGES_LEAD_VALUE = -math.inf


class LeadExtractor:
    def __init__(self):
        self._last_seq_numbers: Dict[Address, int] = dict()

    def extract_lead(self, data: bytearray, source: Address):
        sequence_number = extract_uint32(data)
        if sequence_number is not None:
            return self.compute_lead_and_update_last_sequence_number(source, sequence_number)
        else:
            return None

    def compute_lead_and_update_last_sequence_number(self, source: Address, seq_no: int) -> int:
        last_seq_no = self._last_seq_numbers.get(source, seq_no - 1)
        self._last_seq_numbers[source] = max(last_seq_no, seq_no)
        return seq_no - last_seq_no
