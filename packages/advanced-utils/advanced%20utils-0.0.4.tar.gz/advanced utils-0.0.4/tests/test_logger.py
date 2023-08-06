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
from freezegun import freeze_time

from advanced_utils.logger import Logger


ROOT_DIR = os.getcwd()
LOG_DIR = f"{ROOT_DIR}/logs"


class TestLogger(unittest.TestCase):

    @freeze_time("2012-01-01")
    def setUp(self):
        print('setUp...')

        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)

        self.logger = Logger('default')
        self.logger.info('at set up')

    def tearDown(self):
        print('tearDown...')

        # if os.path.exists(LOG_DIR):
        #     os.rmdir(LOG_DIR)

    def test(self):
        self.logger.info('456')
