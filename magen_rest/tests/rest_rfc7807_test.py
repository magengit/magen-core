#! /usr/bin/python3
"""Rest RFC7807 Test Suite"""
import json
import unittest

from magen_rest_apis.rest_rfc7807 import RestRfc7807


__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class RestRfc7807Test(unittest.TestCase):
    """Rest RFC7807 Test"""
    error_report_exp = {"title": "e", "instance": "s", "status": "s", "detail": "t", "type_uri": "t"}
    error_report_json_str_exp = """{"detail": "t", "instance": "s", "status": "s", "title": "e", "type_uri": "t"}"""

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        """
        This function prepares the system for running tests
        """
        pass

    def tearDown(self):
        pass

    def test_Json_dumps(self):
        error_report = RestRfc7807("t", "e", "s", "t", "s")
        error_report_json_str = json.dumps(error_report, default=RestRfc7807.to_dict, sort_keys=True)
        self.assertEqual(error_report_json_str, RestRfc7807Test.error_report_json_str_exp,
                         "Failed to serialize to JSON string")

    def test_To_dict(self):
        error_report = RestRfc7807("t", "e", "s", "t", "s")
        error_report_dict = error_report.to_dict()
        self.assertEqual(error_report_dict, RestRfc7807Test.error_report_exp, "Failed to serialize to dict")
