import json
import os
import sys
import unittest
from http import HTTPStatus

from flask import Flask

import magen_core_test_env

from magen_rest_apis.rest_server_apis import RestServerApis


__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"

rest_response = """
{
  "response": {
    "cause": "Test Successful",
    "success": true,
    "test_uuid": "74c1c6ff-c266-43a6-9d14-82dca05cb6df"
  },
  "status": 504,
  "title": "test_RestRespondOK"
}"""


class RestServerApisTest(unittest.TestCase):
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

    def test_RestRespondOK(self):
        result = {
            "success": True,
            "test_uuid": RestServerApisTest.TEST_UUID,
            "cause": "Test Successful"
        }
        with self.__class__.app.test_request_context():
            http_response = RestServerApis.respond(HTTPStatus.GATEWAY_TIMEOUT, "test_RestRespondOK", result)
            self.assertEqual(json.loads(http_response.response[0]), json.loads(rest_response))

    def test_RestRespondNotOK(self):
        result = {
            "success": True,
            "test_uuid": RestServerApisTest.TEST_UUID,
            "cause": "Test Successful"
        }
        with self.assertRaises(RuntimeError) as context:
            RestServerApis.respond(http_status=HTTPStatus.GATEWAY_TIMEOUT, title="test_RestRespondOK",
                                   response=result)
