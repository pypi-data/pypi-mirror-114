#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# vim:ts=4
# vim:expandtab
#
# Copyright (C) 2016 JohnZ.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
通用随机方法
"""

import random

def random_by_weight(items: dict, total_weight: int=0) -> tuple:
    """
    {"key1": value1, "key2": value2}
    按照数据的权重，随机一个 key
    数据类型必须是
        key: string
        value: int
    """

    total = 0
    if total_weight <= 0:
        for key in items:
            value = items[key]
            if not isinstance(value, int):
                value = int(value)

            total += value
    else:
        total = total_weight

    random_number = random.randint(0, total - 1)
    cursor = 0
    selected_key = None
    selected_value = None

    for key in items:
        value = items[key]
        if not isinstance(value, int):
            value = int(value)
        weight = value
        min_limit = cursor
        max_limit = cursor + weight

        if random_number >= min_limit and random_number < max_limit:
            selected_key = key
            selected_value = items[key]
            break
        else:
            cursor += weight
            continue

    return (selected_key, selected_value)

