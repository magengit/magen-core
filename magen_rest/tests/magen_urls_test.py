import os
import sys
import unittest

from flask import Flask

import magen_core_test_env

from magen_rest_apis.magen_urls import MagenUrls

print(sys.path)

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class MagenUrlsTest(unittest.TestCase):
    TEST_UUID = "74c1c6ff-c266-43a6-9d14-82dca05cb6df"
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)

    def setUp(self):
        """
        This function prepares the system for running tests
        """
        pass

    def tearDown(self):
        pass

    def test_MagenUrlsJson(self):
        magen_urls = MagenUrls()
        self.assertEqual(magen_urls.get_json_headers, {'Accept': 'application/json'})
        self.assertEqual(magen_urls.put_json_headers,
                         {'content-type': 'application/json', 'Accept': 'application/json'})
