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
import codecs
import time
import datetime
import glob
import logging
from logging.handlers import BaseRotatingHandler


# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

FORMATTER = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(filename)s[%(lineno)d] %(message)s', '%Y-%m-%d %H:%M:%S')
SUFFIX = '%Y-%m-%d'


class MultiProcessSafeDailyRotatingFileHandler(BaseRotatingHandler):
    """Similar with `logging.TimedRotatingFileHandler`, while this one is
    - Multi process safe
    - Rotate at midnight only
    - Utc not supported
    """
    def __init__(self, filename, suffix, backupCount=3, encoding=None, delay=False, utc=False, **kwargs):
        self.utc = utc
        self.suffix = suffix
        self.baseFilename = filename
        self.backupCount = backupCount
        self.currentFileName = self._compute_fn()

        BaseRotatingHandler.__init__(self, filename, 'a', encoding, delay)

    def shouldRollover(self, record):
        if self.currentFileName != self._compute_fn():
            return True
        return False

    def doRollover(self):
        # 关闭旧的文件
        if self.stream:
            self.stream.close()
            self.stream = None

        # 清理多余的日志文件
        backup_date = []
        now = datetime.datetime.now()
        for i in range(self.backupCount):
            delta = datetime.timedelta(days=i)
            backup_date_str = (now - delta).strftime(self.suffix)
            backup_date.append(backup_date_str)

        for file_name in glob.glob(self.baseFilename + '.*'):
            basename_suffix = file_name.split('.')[-1]

            if basename_suffix not in backup_date:
                if os.path.exists(file_name):
                    try:
                        os.remove(file_name)
                    except OSError:
                        pass

        # 设置新文件名
        self.currentFileName = self._compute_fn()

    def _compute_fn(self):
        return self.baseFilename + "." + time.strftime(self.suffix, time.localtime())

    def _open(self):
        if self.encoding is None:
            stream = open(self.currentFileName, self.mode)
        else:
            stream = codecs.open(self.currentFileName, self.mode, self.encoding)

        # simulate file name structure of `logging.TimedRotatingFileHandler`
        if os.path.exists(self.baseFilename):
            try:
                os.remove(self.baseFilename)
            except OSError:
                pass

        if os.path.islink(self.baseFilename):
            try:
                os.unlink(self.baseFilename)
            except OSError:
                pass

        try:
            os.symlink(self.currentFileName, self.baseFilename)
        except OSError:
            pass
        return stream


class Logger(logging.Logger):
    """
    Logger
    """
    LogDir = None
    LogSuffix = SUFFIX
    LogLevel = DEBUG

    @classmethod
    def SetConfig(cls, log_dir: str, suffix=SUFFIX, level=DEBUG):
        """
        Set Logger default config.
        """
        cls.LogDir = log_dir
        cls.LogSuffix = suffix
        cls.LogLevel = level

    def __init__(self, name='default', level=None, backup_count=3):
        self.name = name

        if level is None:
            self.level = Logger.LogLevel
        else:
            self.level = level

        self.backup_count = backup_count

        if Logger.LogDir is None:
            # set default dir to python command + logs dir
            root_dir = os.getcwd()
            Logger.LogDir = root_dir + '/logs'

        logging.Logger.__init__(self, self.name, level=level)
        self.__setFileHandler__(level)

    def __setFileHandler__(self, level):
        file_name = os.path.join(Logger.LogDir, f"{self.name}.log")

        file_handler = MultiProcessSafeDailyRotatingFileHandler(
            filename=file_name,
            suffix=Logger.LogSuffix,
            backupCount=self.backup_count
        )
        file_handler.suffix = Logger.LogSuffix
        file_handler.setFormatter(FORMATTER)

        self.addHandler(file_handler)

        # debug redirect to console
        if level == DEBUG:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(FORMATTER)
            self.addHandler(console_handler)
