#! /usr/bin/python3

import unittest
from datetime import datetime
from pytz import timezone
from magen_utils_apis import datetime_api

import os

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
    	self.fmt = "%Y-%m-%d'T'%H:%M:%S %Z%z"
    	str_timedate = datetime.now(timezone('UTC'))
    	now_utc = str_timedate.strftime(self.fmt)
    	timestamp = datetime_api.datetime_utc_parse(now_utc)
    	self.assertEquals(timestamp, '')

    def test_datetime_parse_iso8601_string_to_utc(self):
    	self.fmt = "%Y-%m-%d'T'%H:%M:%S %Z%z"
    	str_timedate = datetime.now(timezone('UTC'))
    	now_utc = str_timedate.strftime(self.fmt)
    	timestamp = datetime_api.datetime_parse_iso8601_string_to_utc(now_utc)
        print (tim)
    	self.assertEquals(timestamp, '')