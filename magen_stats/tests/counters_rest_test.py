#! /usr/bin/python3
import unittest
import time

from multiprocessing import Process

from flask import Flask

import magen_core_test_env
from magen_rest_apis.rest_client_apis import RestClientApis

from magen_statistics_server.source_counter_rest_api import sourced_counters
from magen_statistics_server.counter_urls import CounterUrls
from magen_statistics_server.metrics_server import MetricsApp
from magen_statistics_api.counter_metric_api import CounterAPI
from .counter_test_data import MULTIPLE_COUNTERS_DATA, SINGLE_COUNTER_DATA, \
    DETAILED_SINGLE_COUNTER_RESPONSE, REST_REQUEST_COUNTERS_RESPONSE, SINGLE_COUNTER_GET_RESP, \
    SINGLE_OK_COUNTER_GET_RESP, SINGLE_NOT_FOUND_COUNTER_GET_RESP, MULTIPLE_COUNTERS_GET, SINGLE_COUNTER_DATA_NOT_FOUND

__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__email__ = "alifar@cisco.com"
__date__ = "10/24/2016"


TEST_HOST = "0.0.0.0"
TEST_PORT = 9999


def url_routes(app):
    endpoints = [rule.rule for rule in app.url_map.iter_rules()
                 if rule.endpoint != 'static']
    return dict(api_endpoints=endpoints)


class TestCounterRESTApi(unittest.TestCase):
    """
    Counter Rest API will use Ingestion service as a source for Counter manipulations
    """
    server_app = None
    counter_urls = None
    server_process = None
    test_source = "ingestion"

    @classmethod
    def setUpClass(cls):
        """
        Set up for Tests. Initiates instances for URLs

        :rtype: void
        """
        cls.server_app = Flask(__name__)
        cls.server_app.register_blueprint(sourced_counters)
        cls.server_app.config['TESTING'] = True

        test_host_port = TEST_HOST+":"+str(TEST_PORT)

        server_args = {
            'host': TEST_HOST,
            'port': TEST_PORT,
            'use_reloader': False
        }

        cls.server_app.debug = True

        cls.server_process = Process(target=cls.server_app.run, kwargs=server_args)
        cls.server_process.start()
        time.sleep(1)
        cls.counter_urls = CounterUrls(test_host_port, cls.test_source)

    def setUp(self):
        CounterAPI.delete_counters(TestCounterRESTApi.test_source)

    def tearDown(self):
        """Tear down Deletion of all Counters"""
        delete_resp = RestClientApis.http_delete_and_get_check(
            TestCounterRESTApi.counter_urls.counters_url
        )
        self.assertTrue(delete_resp.success)

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()

    def test_MetricsApp(self):
        """
        Checks Singleton property of Metrics Flask Application class

        :rtype: void
        """
        app_instance_one = MetricsApp()
        app_instance_two = MetricsApp()
        self.assertIs(app_instance_one, app_instance_two)
        app_instance_one.metrics = 1
        self.assertTrue(isinstance(app_instance_one.metrics, object))

    def test_SingleCounterCreate(self):
        """
        Creates a single Unflavored Counter with POST request,
        then deletes it

        :rtype: void
        """
        print()
        print("+++++++++Single Counter Creation Test+++++++++")
        post_resp = RestClientApis.http_post_and_compare_get_resp(
                TestCounterRESTApi.counter_urls.counters_url,
                SINGLE_COUNTER_DATA,
                SINGLE_COUNTER_GET_RESP
        )
        self.assertTrue(post_resp.success)

    def test_SingleRestResponseCounterCreate(self):
        """
        Creates RestResponse counter with POST request

        :rtype: void
        """
        print()
        print("+++++++++Single RestResponse Counter Creation Test+++++++++")
        post_resp = RestClientApis.http_post_and_compare_get_resp(
            TestCounterRESTApi.counter_urls.restresponse_ok_counter_url,
            SINGLE_COUNTER_DATA,
            SINGLE_OK_COUNTER_GET_RESP
        )
        self.assertTrue(post_resp.success)

    def test_SingleCounterCreateWithFlavor(self):
        """
        Creates Flavored counter by providing flavor inside request body with POST request

        :rtype: void
        """
        print()
        print("+++++++++Single Flavored Counter Creation from dict Test+++++++++")
        post_resp = RestClientApis.http_post_and_compare_get_resp(
                TestCounterRESTApi.counter_urls.counters_url,
                SINGLE_COUNTER_DATA_NOT_FOUND,
                SINGLE_NOT_FOUND_COUNTER_GET_RESP
            )
        self.assertTrue(post_resp.success)

    def test_UnflavoredCountersCreate(self):
        """
        Post and Get counters summarized information for unflavored counters

        :rtype: void
        """
        print()
        print("+++++++++Multiple Counters Creation Test+++++++++")
        post_resp = RestClientApis.http_post_and_compare_get_resp(
            TestCounterRESTApi.counter_urls.counters_url,
            MULTIPLE_COUNTERS_DATA,
            MULTIPLE_COUNTERS_GET
        )
        self.assertTrue(post_resp.success)

    def test_FlavoredCounterDetailedGet(self):
        """
        Get details for unflavored counter

        :rtype: void
        """
        print()
        print("+++++++++Counter Get Test+++++++++")
        post_resp = RestClientApis.http_post_and_check_success(
            TestCounterRESTApi.counter_urls.restresponse_ok_counter_url,
            SINGLE_COUNTER_DATA
        )
        self.assertTrue(post_resp.success)
        get_resp = RestClientApis.http_get_and_compare_resp(
            TestCounterRESTApi.counter_urls.restresponse_ok_counter_url,
            DETAILED_SINGLE_COUNTER_RESPONSE
        )
        self.assertTrue(get_resp.success)

    def test_RestRequestCountersSummaryGet(self):
        """
        Get Summarized info about RestResponse counters

        :rtype: void
        """
        print()
        print("+++++++++RestRequest Counters Get Test+++++++++")
        post_resp = RestClientApis.http_post_and_check_success(
            TestCounterRESTApi.counter_urls.counters_url,
            MULTIPLE_COUNTERS_DATA
        )
        self.assertTrue(post_resp.success)
        get_resp = RestClientApis.http_get_and_compare_resp(
            TestCounterRESTApi.counter_urls.restrequest_counters_url,
            REST_REQUEST_COUNTERS_RESPONSE
        )
        self.assertTrue(get_resp.success)
