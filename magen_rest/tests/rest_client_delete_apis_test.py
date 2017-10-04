#! /usr/bin/python3
"""Rest Client Delete API Test Suite"""
import json
import unittest
from http import HTTPStatus

import responses

from magen_rest.magen_rest_apis.rest_client_apis import RestClientApis
from .rest_client_apis_test_messages import MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE, \
    MAGEN_SINGLE_ASSET_FINANCE_GET_RESP

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class RestClientDeleteApisTest(unittest.TestCase):
    """Rest Client Delete API Test"""
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
        return True, HTTPStatus.OK.phrase, HTTPStatus.OK

    @staticmethod
    def my_func_test_fail(*args, **kwargs):
        """
        Function indicates custom function for check all Client API
        :param args: any type of parameters that this funtion works with
        :param kwargs: any type of parameters that this funtion works with
        """
        return False, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, HTTPStatus.INTERNAL_SERVER_ERROR

    @responses.activate
    def test_Http_delete_ok(self):
        responses.add(responses.DELETE, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=200)
        resp_obj = RestClientApis.http_delete_and_check_success(RestClientDeleteApisTest.LOCATION_URL,
                                                                 RestClientDeleteApisTest.my_func_test_ok)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_Http_delete_fail_my_func(self):
        responses.add(responses.DELETE, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=200)
        resp_obj = RestClientApis.http_delete_and_check_success(RestClientDeleteApisTest.LOCATION_URL,
                                                                RestClientDeleteApisTest.my_func_test_fail)
        self.assertFalse(resp_obj.success)

    @responses.activate
    def test_Http_delete_ok_no_func(self):
        responses.add(responses.DELETE, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=200)
        resp_obj = RestClientApis.http_delete_and_check_success(RestClientDeleteApisTest.LOCATION_URL)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_http_delete_204(self):
        responses.add(responses.DELETE, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=HTTPStatus.NO_CONTENT)
        resp_obj = RestClientApis.http_delete_and_check_success(RestClientDeleteApisTest.LOCATION_URL)
        self.assertTrue(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.NO_CONTENT, "")

    @responses.activate
    def test_http_delete_500(self):
        responses.add(responses.DELETE, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=500)
        resp_obj = RestClientApis.http_delete_and_check_success(RestClientDeleteApisTest.LOCATION_URL)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR, "Status code does not match")

    @responses.activate
    def test_http_delete_400(self):
        responses.add(responses.DELETE, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=400)
        resp_obj = RestClientApis.http_delete_and_check_success(RestClientDeleteApisTest.LOCATION_URL)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.BAD_REQUEST, "Status code does not match")

    def test_Http_delete_invalid_schema(self):
        url = "invalid://httpbin.org/status/200"
        resp_obj = RestClientApis.http_delete_and_check_success(url, RestClientDeleteApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.BAD_REQUEST, "Status code does not match")

    def test_Http_delete_connection_timeout(self):
        url = RestClientDeleteApisTest.UNREACHABLE_HOST
        resp_obj = RestClientApis.http_delete_and_check_success(url, RestClientDeleteApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.SERVICE_UNAVAILABLE, "Status code does not match")

    def test_Http_delete_connection_error(self):
        url = RestClientDeleteApisTest.NO_WEB_SERVER_RUNNING_HOST
        resp_obj = RestClientApis.http_delete_and_check_success(url, RestClientDeleteApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.SERVICE_UNAVAILABLE, "Status code does not match")

    @responses.activate
    def test_Http_delete_and_get_check_ok(self):
        """
        This test is ok when it fails
        """
        responses.add(responses.DELETE, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=200)
        responses.add(responses.GET, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=404)
        resp_obj = RestClientApis.http_delete_and_get_check(RestClientDeleteApisTest.LOCATION_URL)
        self.assertTrue(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.OK, "Status code does not match")

    @responses.activate
    def test_Http_delete_and_get_check_fail_delete(self):
        responses.add(responses.DELETE, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=500)
        resp_obj = RestClientApis.http_delete_and_get_check(RestClientDeleteApisTest.LOCATION_URL)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR, "Status code does not match")

    @responses.activate
    def test_Http_delete_and_get_check_fail_get_ok(self):
        """
        Server says magen_resource was deleted but the GET returns ok.
        """
        responses.add(responses.DELETE, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE), status=200)
        responses.add(responses.GET, RestClientDeleteApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_delete_and_get_check(RestClientDeleteApisTest.LOCATION_URL)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR, "Status code does not match")
