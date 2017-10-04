#! /usr/bin/python3
"""Rest Client GET API Test Suite"""
import json
import unittest
from http import HTTPStatus

import responses

from ..magen_rest_apis.rest_client_apis import RestClientApis
from .rest_client_apis_test_messages import MAGEN_SINGLE_ASSET_FINANCE_GET_RESP


__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class RestClientGetApisTest(unittest.TestCase):
    """Rest Client GET API Test"""
    UNREACHABLE_HOST = "http://127.0.0.2"
    NO_WEB_SERVER_RUNNING_HOST = "http://127.0.0.1"
    INVALID_URL = "https://httpb  in.org/"
    MAGEN_BASE_URL = 'http://magen.cisco.com/service/v2/resources/magen_resource/'
    LOCATION_URL = MAGEN_BASE_URL + "74c1c6ff-c266-43a6-9d14-82dca05cb6df/"

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

    @staticmethod
    def my_func_test_ok(*args, **kwargs):
        """
        Function indicates custom function for check all Client API
        :param args: any type of parameters that this funtion works with
        :param kwargs: any type of parameters that this funtion works with
        """
        return True

    @staticmethod
    def my_func_test_fail(*args, **kwargs):
        """
        Function indicates custom function for check all Client API
        :param args: any type of parameters that this funtion works with
        :param kwargs: any type of parameters that this funtion works with
        """
        return False

    @responses.activate
    def test_Http_get_and_check_ok(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_get_and_check_success(RestClientGetApisTest.LOCATION_URL,
                                                             RestClientGetApisTest.my_func_test_ok)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_Http_get_and_check_fail(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_get_and_check_success(RestClientGetApisTest.LOCATION_URL,
                                                             RestClientGetApisTest.my_func_test_fail)
        self.assertFalse(resp_obj.success)

    @responses.activate
    def test_Http_get_and_check_no_func(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_get_and_check_success(RestClientGetApisTest.LOCATION_URL)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_http_get_and_check_500(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=500)
        resp_obj = RestClientApis.http_get_and_check_success(RestClientGetApisTest.LOCATION_URL,
                                                             RestClientGetApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR, "Status code does not match")

    @responses.activate
    def test_http_get_and_check_400(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=400)
        resp_obj = RestClientApis.http_get_and_check_success(RestClientGetApisTest.LOCATION_URL,
                                                             RestClientGetApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.BAD_REQUEST, "Status code does not match")

    def test_Http_get_and_check_invalid_schema(self):
        url = "invalid://httpbin.org/status/200"
        resp_obj = RestClientApis.http_get_and_check_success(url, RestClientGetApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.BAD_REQUEST, "Status code does not match")

    def test_Http_get_and_check_connection_timeout(self):
        url = RestClientGetApisTest.UNREACHABLE_HOST
        resp_obj = RestClientApis.http_get_and_check_success(url, RestClientGetApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.SERVICE_UNAVAILABLE, "Status code does not match")

    def test_Http_get_and_check_connection_error(self):
        url = RestClientGetApisTest.NO_WEB_SERVER_RUNNING_HOST
        resp_obj = RestClientApis.http_get_and_check_success(url, RestClientGetApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.SERVICE_UNAVAILABLE, "Status code does not match")

    @responses.activate
    def test_http_get_and_compare_resp_ok(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_get_and_compare_resp(RestClientGetApisTest.LOCATION_URL,
                                                            MAGEN_SINGLE_ASSET_FINANCE_GET_RESP,
                                                            RestClientGetApisTest.my_func_test_ok)
        self.assertTrue(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.OK, "Status code does not match")

    @responses.activate
    def test_http_get_and_compare_resp_ok_default_compare(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_get_and_compare_resp(RestClientGetApisTest.LOCATION_URL,
                                                            MAGEN_SINGLE_ASSET_FINANCE_GET_RESP)
        self.assertTrue(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.OK, "Status code does not match")

    @responses.activate
    def test_http_get_and_compare_resp_fail_500(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=500)
        resp_obj = RestClientApis.http_get_and_compare_resp(RestClientGetApisTest.LOCATION_URL,
                                                            MAGEN_SINGLE_ASSET_FINANCE_GET_RESP,
                                                            RestClientGetApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR, "Status code does not match")

    @responses.activate
    def test_http_get_and_compare_resp_fail_my_function(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_get_and_compare_resp(RestClientGetApisTest.LOCATION_URL,
                                                            MAGEN_SINGLE_ASSET_FINANCE_GET_RESP,
                                                            RestClientGetApisTest.my_func_test_fail)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR, "Status code does not match")

    @responses.activate
    def test_http_get_and_compare_resp_fail_default_compare(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_get_and_compare_resp(RestClientGetApisTest.LOCATION_URL,
                                                            {"response": "will not match"})
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR, "Status code does not match")

    @responses.activate
    def test_http_get_and_compare_resp_fail_default_compare_bad_data(self):
        responses.add(responses.GET, RestClientGetApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_get_and_compare_resp(RestClientGetApisTest.LOCATION_URL,
                                                            '333')
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR, "Status code does not match")
