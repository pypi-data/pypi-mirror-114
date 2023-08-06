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

import os
import unittest

from advanced_utils.random import random_by_weight



class TestRandom(unittest.TestCase):

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')

    def test(self):
        test_dict = {'a': 100, 'b': 0}
        key, value = random_by_weight(test_dict, 100)

        assert key == 'a'
