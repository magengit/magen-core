#! /usr/bin/python3
"""Rest Client PUT API Test Suite"""
import json
import unittest
from http import HTTPStatus
import responses

from .rest_client_apis_test_messages import MAGEN_SINGLE_ASSET_FINANCE_POST, \
    MAGEN_SINGLE_ASSET_FINANCE_GET_RESP, MAGEN_SINGLE_ASSET_GET_RESP_404
from .rest_client_apis_test_messages import MAGEN_SINGLE_ASSET_FINANCE_POST_RESP
from ..magen_rest_apis.rest_client_apis import RestClientApis

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class RestClientPutApisTest(unittest.TestCase):
    """Rest Client PUT API Test"""
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
    def test_Http_put_and_compare_get_resp(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': RestClientPutApisTest.LOCATION_URL},
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        responses.add(responses.GET, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_put_and_compare_get_resp(RestClientPutApisTest.LOCATION_URL,
                                                                MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                                MAGEN_SINGLE_ASSET_FINANCE_GET_RESP,
                                                                RestClientPutApisTest.my_func_test_ok)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_Http_put_and_compare_get_resp_fail_get(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': RestClientPutApisTest.LOCATION_URL},
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        responses.add(responses.GET, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_GET_RESP_404), status=404)
        resp_obj = RestClientApis.http_put_and_compare_get_resp(RestClientPutApisTest.LOCATION_URL,
                                                                MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                                MAGEN_SINGLE_ASSET_FINANCE_GET_RESP,
                                                                RestClientPutApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)

    @responses.activate
    def test_Http_put_and_compare_get_resp_fail_no_json(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': RestClientPutApisTest.LOCATION_URL},
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        responses.add(responses.GET, RestClientPutApisTest.LOCATION_URL,
                      json=dict(), status=200)
        resp_obj = RestClientApis.http_put_and_compare_get_resp(RestClientPutApisTest.LOCATION_URL,
                                                                MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                                MAGEN_SINGLE_ASSET_FINANCE_GET_RESP,
                                                                RestClientPutApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)

    @responses.activate
    def test_Http_put_and_compare_get_resp_no_func(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': RestClientPutApisTest.LOCATION_URL},
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        responses.add(responses.GET, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_GET_RESP), status=200)
        resp_obj = RestClientApis.http_put_and_compare_get_resp(RestClientPutApisTest.LOCATION_URL,
                                                                MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                                MAGEN_SINGLE_ASSET_FINANCE_GET_RESP)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_Http_put_and_compare_get_resp_fail_no_location(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        responses.add(responses.GET, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_GET_RESP_404), status=404)
        resp_obj = RestClientApis.http_put_and_compare_get_resp(RestClientPutApisTest.LOCATION_URL,
                                                                MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                                MAGEN_SINGLE_ASSET_FINANCE_GET_RESP,
                                                                RestClientPutApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)

    @responses.activate
    def test_Http_put_and_compare_get_resp_fail_my_function(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': RestClientPutApisTest.LOCATION_URL},
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        responses.add(responses.GET, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_GET_RESP_404), status=404)
        resp_obj = RestClientApis.http_put_and_compare_get_resp(RestClientPutApisTest.LOCATION_URL,
                                                                MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                                MAGEN_SINGLE_ASSET_FINANCE_GET_RESP,
                                                                RestClientPutApisTest.my_func_test_fail)
        self.assertFalse(resp_obj.success)

    @responses.activate
    def test_Http_put_ok(self):
        location_url = RestClientPutApisTest.LOCATION_URL + "74c1c6ff-c266-43a6-9d14-82dca05cb6df/"
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': location_url}, json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=200)
        resp_obj = RestClientApis.http_put_and_check_success(RestClientPutApisTest.LOCATION_URL,
                                                             MAGEN_SINGLE_ASSET_FINANCE_POST)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_Http_put_fail(self):
        location_url = RestClientPutApisTest.LOCATION_URL + "74c1c6ff-c266-43a6-9d14-82dca05cb6df/"
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': location_url}, json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        resp_obj = RestClientApis.http_put_and_check_success(RestClientPutApisTest.LOCATION_URL,
                                                             MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                             my_function=RestClientPutApisTest.my_func_test_fail)
        self.assertFalse(resp_obj.success)

    @responses.activate
    def test_Http_put_no_func(self):
        location_url = RestClientPutApisTest.LOCATION_URL + "74c1c6ff-c266-43a6-9d14-82dca05cb6df/"
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': location_url}, json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        resp_obj = RestClientApis.http_put_and_check_success(RestClientPutApisTest.LOCATION_URL,
                                                             MAGEN_SINGLE_ASSET_FINANCE_POST)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_http_put_500(self):
        location_url = RestClientPutApisTest.LOCATION_URL + "74c1c6ff-c266-43a6-9d14-82dca05cb6df/"
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': location_url}, json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=500)
        resp_obj = RestClientApis.http_put_and_check_success(RestClientPutApisTest.LOCATION_URL,
                                                             MAGEN_SINGLE_ASSET_FINANCE_POST)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR, "Status code does not match")

    @responses.activate
    def test_http_put_400(self):
        location_url = RestClientPutApisTest.LOCATION_URL + "74c1c6ff-c266-43a6-9d14-82dca05cb6df/"
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL, adding_headers={
            'Location': location_url}, json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=400)
        resp_obj = RestClientApis.http_put_and_check_success(RestClientPutApisTest.LOCATION_URL,
                                                             MAGEN_SINGLE_ASSET_FINANCE_POST)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.BAD_REQUEST, "Status code does not match")

    def test_Http_put_invalid_schema(self):
        url = "invalid://httpbin.org/status/200"
        resp_obj = RestClientApis.http_put_and_check_success(url, MAGEN_SINGLE_ASSET_FINANCE_POST_RESP,
                                                             RestClientPutApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.BAD_REQUEST, "Status code does not match")

    def test_Http_put_connection_timeout(self):
        url = RestClientPutApisTest.UNREACHABLE_HOST
        resp_obj = RestClientApis.http_put_and_check_success(url, MAGEN_SINGLE_ASSET_FINANCE_POST_RESP,
                                                             RestClientPutApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.SERVICE_UNAVAILABLE, "Status code does not match")

    def test_Http_put_connection_error(self):
        url = RestClientPutApisTest.NO_WEB_SERVER_RUNNING_HOST
        resp_obj = RestClientApis.http_put_and_check_success(url, MAGEN_SINGLE_ASSET_FINANCE_POST_RESP,
                                                             RestClientPutApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.SERVICE_UNAVAILABLE, "Status code does not match")

    @responses.activate
    def test_Http_put_and_compare_resp(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        resp_obj = RestClientApis.http_put_and_compare_resp(RestClientPutApisTest.LOCATION_URL,
                                                            MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                            MAGEN_SINGLE_ASSET_FINANCE_POST_RESP,
                                                            RestClientPutApisTest.my_func_test_ok)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_Http_put_and_compare_resp_no_func(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        resp_obj = RestClientApis.http_put_and_compare_resp(RestClientPutApisTest.LOCATION_URL,
                                                            MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                            MAGEN_SINGLE_ASSET_FINANCE_POST_RESP)
        self.assertTrue(resp_obj.success)

    @responses.activate
    def test_Http_put_and_compare_resp_fail_no_json(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL,
                      json=dict(), status=201)
        resp_obj = RestClientApis.http_put_and_compare_resp(RestClientPutApisTest.LOCATION_URL,
                                                            MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                            MAGEN_SINGLE_ASSET_FINANCE_POST_RESP,
                                                            RestClientPutApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR)

    @responses.activate
    def test_Http_put_and_compare_resp_fail(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=500)
        resp_obj = RestClientApis.http_put_and_compare_resp(RestClientPutApisTest.LOCATION_URL,
                                                            MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                            MAGEN_SINGLE_ASSET_FINANCE_POST_RESP,
                                                            RestClientPutApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)
        self.assertEqual(resp_obj.http_status, HTTPStatus.INTERNAL_SERVER_ERROR)

    @responses.activate
    def test_Http_put_and_compare_resp_fail_put(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=500)
        resp_obj = RestClientApis.http_put_and_compare_get_resp(RestClientPutApisTest.LOCATION_URL,
                                                                MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                                MAGEN_SINGLE_ASSET_FINANCE_POST_RESP,
                                                                RestClientPutApisTest.my_func_test_ok)
        self.assertFalse(resp_obj.success)

    @responses.activate
    def test_Http_put_and_compare_resp_fail_my_function(self):
        responses.add(responses.PUT, RestClientPutApisTest.LOCATION_URL,
                      json=json.loads(MAGEN_SINGLE_ASSET_FINANCE_POST_RESP), status=201)
        resp_obj = RestClientApis.http_put_and_compare_get_resp(RestClientPutApisTest.LOCATION_URL,
                                                                MAGEN_SINGLE_ASSET_FINANCE_POST,
                                                                MAGEN_SINGLE_ASSET_FINANCE_GET_RESP,
                                                                RestClientPutApisTest.my_func_test_fail)
        self.assertFalse(resp_obj.success)
