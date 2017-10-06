#! /usr/bin/python3
"""Test Suit for Rest API of Magen Metrics"""
import unittest

from flask import Flask
from http import HTTPStatus
import json

from magen_utils_apis.compare_utils import default_full_compare

from magen_statistics_server.source_counter_rest_api import sourced_counters
from magen_statistics_server.counter_urls import CounterUrls
from magen_statistics_server.metrics_server import MetricsApp
from magen_statistics_api.counter_metric_api import CounterAPI
from .counter_test_data import MULTIPLE_COUNTERS_DATA, SINGLE_COUNTER_DATA, \
    DETAILED_SINGLE_COUNTER_RESPONSE, REST_REQUEST_COUNTERS_RESPONSE, SINGLE_COUNTER_GET_RESP, \
    SINGLE_OK_COUNTER_GET_RESP, SINGLE_NOT_FOUND_COUNTER_GET_RESP, MULTIPLE_COUNTERS_GET, \
    SINGLE_COUNTER_DATA_NOT_FOUND, SINGLE_COUNTER_POST_RESP, SINGLE_COUNTER_RESTRESP_POST_RESP, \
    SINGLE_COUNTER_FLAVORED_POST_RESP, MULTIPLE_COUNTERS_POST_RESP

__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__email__ = "alifar@cisco.com"
__date__ = "10/24/2016"


TEST_HOST = "0.0.0.0"
TEST_PORT = 9999


class TestCounterRESTApi(unittest.TestCase):
    """
    Counter Rest API will use Ingestion service as a source for Counter manipulations
    """
    counter_urls = None
    test_source = "ingestion"

    @classmethod
    def setUpClass(cls):
        """
        Set up for Tests. Initiates instances for URLs

        :rtype: void
        """
        test_host_port = TEST_HOST+":"+str(TEST_PORT)
        cls.counter_urls = CounterUrls(test_host_port, cls.test_source)

    def setUp(self):
        CounterAPI.delete_counters(TestCounterRESTApi.test_source)
        magen_stats_app = Flask(__name__)
        magen_stats_app.config['TESTING'] = True
        magen_stats_app.register_blueprint(sourced_counters)
        self.app = magen_stats_app.test_client()

    def tearDown(self):
        """Tear down Deletion of all Counters"""
        delete_resp = self.app.delete(TestCounterRESTApi.counter_urls.counters_url)
        self.assertEqual(delete_resp.status_code, HTTPStatus.OK)

    def test_metrics_app(self):
        """
        Checks Singleton property of Metrics Flask Application class

        :rtype: void
        """
        app_instance_one = MetricsApp()
        app_instance_two = MetricsApp()
        self.assertIs(app_instance_one, app_instance_two)
        app_instance_one.metrics = 1
        self.assertTrue(isinstance(app_instance_one.metrics, object))

    def test_single_counter_create(self):
        """
        Creates a single Unflavored Counter with POST request,
        then deletes it

        :rtype: void
        """
        print()
        print("+++++++++Single Counter Creation Test+++++++++")
        post_resp = self.app.post(
            TestCounterRESTApi.counter_urls.counters_url,
            data=SINGLE_COUNTER_DATA,
            headers=type(self).counter_urls.put_json_headers
        )
        # Verify Http Status
        self.assertEqual(post_resp.status_code, HTTPStatus.CREATED)
        post_resp_json = json.loads(post_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify that resource was created and uuid was assigned
        self.assertIn('metric_uuid', post_resp_json['response'])
        # Verify returned response skipping dynamic generated fields (metric_uuid)
        self.assertTrue(default_full_compare(SINGLE_COUNTER_POST_RESP, post_resp_json, excluded_keys=['metric_uuid']))

        # Verify that resource is stored properly and available by GET request
        get_resp = self.app.get(TestCounterRESTApi.counter_urls.counters_url)
        get_resp_json = json.loads(get_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify returned response skipping dynamic generated fields (metric_uuid)
        self.assertTrue(default_full_compare(SINGLE_COUNTER_GET_RESP, get_resp_json, excluded_keys=['metric_uuid']))

    def test_SingleRestResponseCounterCreate(self):
        """
        Creates RestResponse counter with POST request

        :rtype: void
        """
        print()
        print("+++++++++Single RestResponse Counter Creation Test+++++++++")
        post_resp = self.app.post(
            TestCounterRESTApi.counter_urls.restresponse_ok_counter_url,
            data=SINGLE_COUNTER_DATA,
            headers=type(self).counter_urls.put_json_headers
        )
        # Verify Http Status
        self.assertEqual(post_resp.status_code, HTTPStatus.CREATED)
        post_resp_json = json.loads(post_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify that resource was created and uuid was assigned
        self.assertIn('metric_uuid', post_resp_json['response'])
        self.assertTrue(default_full_compare(
            SINGLE_COUNTER_RESTRESP_POST_RESP, post_resp_json, excluded_keys=['metric_uuid']
            ))

        # Verify that resource is stored properly and available by GET request
        get_resp = self.app.get(TestCounterRESTApi.counter_urls.restresponse_ok_counter_url)
        get_resp_json = json.loads(get_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify returned response skipping dynamic generated fields (metric_uuid)
        self.assertTrue(default_full_compare(SINGLE_OK_COUNTER_GET_RESP, get_resp_json, excluded_keys=['metric_uuid']))

    def test_SingleCounterCreateWithFlavor(self):
        """
        Creates Flavored counter by providing flavor inside request body with POST request

        :rtype: void
        """
        print()
        print("+++++++++Single Flavored Counter Creation from dict Test+++++++++")
        post_resp = self.app.post(
            TestCounterRESTApi.counter_urls.counters_url,
            data=SINGLE_COUNTER_DATA_NOT_FOUND,
            headers=type(self).counter_urls.put_json_headers
        )
        # Verify Http Status
        self.assertEqual(post_resp.status_code, HTTPStatus.CREATED)
        post_resp_json = json.loads(post_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify that resource was created and uuid was assigned
        self.assertIn('metric_uuid', post_resp_json['response'])
        self.assertTrue(default_full_compare(
            SINGLE_COUNTER_FLAVORED_POST_RESP, post_resp_json, excluded_keys=['metric_uuid']
            ))

        # Verify that resource is stored properly and available by GET request
        get_resp = self.app.get(TestCounterRESTApi.counter_urls.counters_url)
        get_resp_json = json.loads(get_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify returned response skipping dynamic generated fields (metric_uuid)
        self.assertTrue(
            default_full_compare(SINGLE_NOT_FOUND_COUNTER_GET_RESP, get_resp_json, excluded_keys=['metric_uuid']))

    def test_UnflavoredCountersCreate(self):
        """
        Post and Get counters summarized information for unflavored counters

        :rtype: void
        """
        print()
        print("+++++++++Multiple Counters Creation Test+++++++++")
        post_resp = self.app.post(
            TestCounterRESTApi.counter_urls.counters_url,
            data=MULTIPLE_COUNTERS_DATA,
            headers=type(self).counter_urls.put_json_headers
        )
        self.assertEqual(post_resp.status_code, HTTPStatus.CREATED)
        post_resp_json = json.loads(post_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify that resource was created and uuid was assigned
        self.assertIn('metric_uuid', post_resp_json['response'])
        self.assertTrue(default_full_compare(
            MULTIPLE_COUNTERS_POST_RESP, post_resp_json, excluded_keys=['metric_uuid']
        ))

        # Verify that resource is stored properly and available by GET request
        get_resp = self.app.get(TestCounterRESTApi.counter_urls.counters_url)
        get_resp_json = json.loads(get_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify returned response skipping dynamic generated fields (metric_uuid)
        self.assertTrue(
            default_full_compare(MULTIPLE_COUNTERS_GET, get_resp_json, excluded_keys=['metric_uuid']))

    def test_FlavoredCounterDetailedGet(self):
        """
        Get details for unflavored counter

        :rtype: void
        """
        print()
        print("+++++++++Counter Get Test+++++++++")
        post_resp = self.app.post(
            TestCounterRESTApi.counter_urls.restresponse_ok_counter_url,
            data=SINGLE_COUNTER_DATA,
            headers=type(self).counter_urls.put_json_headers
        )
        self.assertEqual(post_resp.status_code, HTTPStatus.CREATED)
        post_resp_json = json.loads(post_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify that resource was created and uuid was assigned
        self.assertIn('metric_uuid', post_resp_json['response'])
        # GET TEST
        get_resp = self.app.get(TestCounterRESTApi.counter_urls.restresponse_ok_counter_url)
        get_resp_json = json.loads(get_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify returned response skipping dynamic generated fields (metric_uuid)
        self.assertTrue(
            default_full_compare(DETAILED_SINGLE_COUNTER_RESPONSE, get_resp_json, excluded_keys=['metric_uuid']))

    def test_RestRequestCountersSummaryGet(self):
        """
        Get Summarized info about RestResponse counters

        :rtype: void
        """
        print()
        print("+++++++++RestRequest Counters Get Test+++++++++")
        post_resp = self.app.post(
            TestCounterRESTApi.counter_urls.counters_url,
            data=MULTIPLE_COUNTERS_DATA,
            headers=type(self).counter_urls.put_json_headers
        )
        self.assertEqual(post_resp.status_code, HTTPStatus.CREATED)
        post_resp_json = json.loads(post_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify that resource was created and uuid was assigned
        self.assertIn('metric_uuid', post_resp_json['response'])
        get_resp = self.app.get(TestCounterRESTApi.counter_urls.restrequest_counters_url)
        get_resp_json = json.loads(get_resp.data.decode("utf-8"))  # decode resp obj - extra step for test_client
        # Verify returned response skipping dynamic generated fields (metric_uuid)
        self.assertTrue(
            default_full_compare(REST_REQUEST_COUNTERS_RESPONSE, get_resp_json, excluded_keys=['metric_uuid']))
