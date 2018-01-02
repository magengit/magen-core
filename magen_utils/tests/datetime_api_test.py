#! /usr/bin/python3

import unittest
from datetime import datetime
from pytz import timezone
from dateutil import tz
from magen_utils_apis import datetime_api

import os
import aniso8601
import magen_core_test_env


__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__email__ = "alifar@cisco.com"
__data__ = "04/05/2017"

class TestDatetimeApi(unittest.TestCase):
    """
    Tests for datetime_api.py
    Execute 'make test' from magen_core directory
    """
    def test_datetime_utc_parse(self):
        self.fmt = "%Y-%m-%dT%H:%M:%SZ"
        str_timedate = datetime.now(timezone('UTC'))
        now_utc = str_timedate.strftime(self.fmt)
        timestamp = datetime_api.datetime_utc_parse(now_utc)
        aniso_date = aniso8601.parse_datetime(now_utc)
        self.assertEquals(timestamp, aniso_date)

    def test_datetime_utc_parse_1(self):
        self.fmt = "%Y-%m-%d %H:%M:%SZ"
        str_timedate = datetime.now(timezone('UTC'))
        now_utc = str_timedate.strftime(self.fmt)
        timestamp = datetime_api.datetime_utc_parse(now_utc)
        aniso_date = aniso8601.parse_datetime(now_utc, delimiter=" ")
        self.assertEquals(timestamp, aniso_date)

    def test_datetime_parse_iso8601_string_to_utc(self):
        fmt = "%Y-%m-%dT%H:%M:%S%z"
        str_time_date = datetime.now(tz.tzlocal())
        to_utc = str_time_date.strftime(fmt)
        timestamp = datetime_api.datetime_parse_iso8601_string_to_utc(to_utc)
        self.assertEquals(timestamp.strftime(fmt), datetime.now(timezone("UTC")).strftime(fmt))
