#! /usr/bin/python3
import unittest

import magen_core_test_env

import magen_statistics_server.counters as counters
from magen_statistics_api.counter_metric_api import get_flavored_counter_instance, CounterAPI
from magen_statistics_api.metric import MetricsCollections
from magen_statistics_api.metric_flavors import RestResponse

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"


class TestCounterApi(unittest.TestCase):
    """
    Tests for External Functional API of Counters
    """
    source = None
    metrics_collections = None

    @classmethod
    def setUpClass(cls):
        """
        Sets up metrics collections and source name

        :rtype: void
        """
        cls.metrics_collections = MetricsCollections()
        cls.source = "TestCounters"

    def setUp(self):
        pass

    def tearDown(self):
        """
        Deletes all metrics in the system after each test

        :rtype: void
        """
        TestCounterApi.metrics_collections.clear()
        self.assertFalse(CounterAPI.get_all_counters())

    def test_Increment(self):
        """
        Test increment method in Counters user's api

        :rtype: void
        """
        counters.increment(RestResponse.OK, TestCounterApi.source)
        counter = get_flavored_counter_instance(RestResponse.OK)
        self.assertIsNotNone(counter)

        value = counter.abs_value

        counters.increment(RestResponse.OK, TestCounterApi.source)
        self.assertEqual(counter.abs_value, value+1)

    def test_Reset(self):
        """
        Test reset method in Counters user's api

        :rtype: void
        """
        self.test_Increment()
        counters.reset(RestResponse.OK)
        counter = get_flavored_counter_instance(RestResponse.OK)
        self.assertEqual(counter.abs_value, 0)

    def test_Delete(self):
        """
        Test delete method in Counters user's api

        :rtype: void
        """
        self.test_Increment()
        counters.delete(RestResponse.OK)
        self.assertIsNone(get_flavored_counter_instance(RestResponse.OK))

