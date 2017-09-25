#! /usr/bin/python3
import unittest

import magen_core_test_env

from magen_statistics_api.counter_metric import Counter
from magen_statistics_api.metric import MetricsCollections
from magen_statistics_api.counter_metric_api import CounterAPI, flavor_str_to_instance
from magen_statistics_api.metric_flavors import RestResponse

from .counter_dict_test_data import SINGLE_COUNTER_DICT, SINGLE_FLAVORED_COUNTER_UNNAMED_DICT, \
    SINGLE_FLAVORED_COUNTER_UNNAMED_CREATED_DICT, SINGLE_FLAVORED_COUNTER_UNNAMED_CREATED_DETAILED_DICT, \
    SINGLE_REST_RESPONSE_COUNTER_DICT, SINGLE_COUNTER_CREATED_DETAILED_DICT, FLAVOR_REST_RESPONSE_TYPE, \
    FLAVOR_REST_RESPONSE_OPT, SINGLE_REST_RESPONSE_COUNTER_CREATED_DETAILED_DICT, FLAVOR_REST_REQUEST_TYPE, \
    FLAVOR_REST_REQUEST_OPT, SINGLE_REST_REQUEST_COUNTER_DICT, SINGLE_REST_REQUEST_COUNTER_CREATED_DETAILED_DICT, \
    MULTIPLE_COUNTERS_CREATED_LIST, SINGLE_REST_REQUEST_COUNTER_CREATED_DICT

__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__email__ = "alifar@cisco.com"
__date__ = "10/24/2016"


class TestCounterApi(unittest.TestCase):
    """
    Tests for Counter internal APIs
    """
    metrics_collections = None
    source = None

    def create_and_check_counter(self, source, counter_dict):
        counter_uuid = CounterAPI.create_counter(source, **counter_dict)
        self.assertIsNotNone(counter_uuid)
        counter_instance = TestCounterApi.metrics_collections.get_metric_by_uuid(
            Counter.__name__,
            counter_uuid
        )
        return counter_instance

    @classmethod
    def setUpClass(cls):
        """
        Method runs before set of tests

        :rtype: void
        """
        cls.metrics_collections = MetricsCollections()
        cls.source = "magen_stats_test"

    def setUp(self):
        """
        Method runs before each test

        :rtype: void
        """
        self.single_counter_instance = self.create_and_check_counter(
            TestCounterApi.source,
            SINGLE_COUNTER_DICT
        )
        self.assertIsNotNone(self.single_counter_instance)

        self.single_restresponse_counter_instance = self.create_and_check_counter(
            TestCounterApi.source,
            SINGLE_REST_RESPONSE_COUNTER_DICT
        )
        self.assertIsNotNone(self.single_restresponse_counter_instance)

        self.single_restrequest_counter_instance = self.create_and_check_counter(
            TestCounterApi.source,
            SINGLE_REST_REQUEST_COUNTER_DICT
        )
        self.assertIsNotNone(self.single_restrequest_counter_instance)

    def tearDown(self):
        """
        Method runs after each test and removes created data

        :rtype: void
        """
        self.single_counter_instance = None
        self.single_restrequest_counter_instance = None
        self.single_restresponse_counter_instance = None
        TestCounterApi.metrics_collections.clear()
        self.assertFalse(CounterAPI.get_all_counters())
        self.assertFalse(CounterAPI.get_flavored_counters("RestResponse.OK"))

    def test_SingleCounterCreation(self):
        """
        Checks correctness of counter creation

        :rtype: void
        """
        print()
        print("+++++++++Single Counter Creation Test+++++++++")
        self.single_counter_instance.provide_detailed_info = True
        counter_dict = self.single_counter_instance.to_dict()
        print("Created counter: ", counter_dict)
        for item in SINGLE_COUNTER_DICT:
            self.assertIn(item, counter_dict)

    def test_SingleCounterUpdate(self):
        """
        Creates a counter and updates it to default and provided value

        :rtype: void
        """
        print()
        print("+++++++++Single Counter Update Test+++++++++")
        print("Created counter: ", self.single_counter_instance.to_dict())
        value_to_increment = 5
        cur_value = self.single_counter_instance.abs_value
        CounterAPI.update_counter(self.single_counter_instance.metric_uuid)
        print("Update Counter by Default ", self.single_counter_instance.abs_value)
        self.assertEqual(self.single_counter_instance.abs_value, cur_value + 1)
        cur_value += 1
        CounterAPI.update_counter(self.single_counter_instance.metric_uuid, value_to_increment)
        print("Update Counter With Given Value ", self.single_counter_instance.abs_value)
        self.assertEqual(self.single_counter_instance.abs_value, cur_value + value_to_increment)

    def test_SingleCounterReset(self):
        """
        Resets counter value to default

        :rtype: void
        """
        print()
        print("+++++++++Single Counter Reset Test+++++++++")
        print("Created counter: ", self.single_counter_instance.to_dict())
        CounterAPI.reset_counter(self.single_counter_instance.metric_uuid)
        self.assertEqual(self.single_counter_instance.abs_value, 0)
        print("Reset value: ", self.single_counter_instance.abs_value)

    def test_SingleCounterRemove(self):
        """
        Removes existing counter from the collection

        :rtype: void
        """
        print()
        print("+++++++++Single Counter Remove Test+++++++++")
        print("Created counter: ", self.single_counter_instance.to_dict())
        CounterAPI.delete_counter(self.single_counter_instance.metric_uuid)
        self.assertIsNone(TestCounterApi.metrics_collections.get_metric_by_uuid(
            Counter.__name__,
            self.single_counter_instance.metric_uuid
        ))

    def test_SingleFlavoredUnnamedCounterDetailedCreate(self):
        """
        Creates and checks single flavored but unnamed counter

        :rtype: void
        """
        unnamed_counter_instance = self.create_and_check_counter(
            TestCounterApi.source,
            SINGLE_FLAVORED_COUNTER_UNNAMED_DICT
        )
        unnamed_counter_instance.provide_detailed_info = True
        counter_dict = unnamed_counter_instance.to_dict()
        print("Created counter: ", counter_dict)
        for item in SINGLE_FLAVORED_COUNTER_UNNAMED_CREATED_DETAILED_DICT:
            self.assertIn(item, counter_dict)

    def test_SingleFlavoredUnnamedCounterCreate(self):
        """
        Creates and checks single flavored but unnamed counter

        :rtype: void
        """
        unnamed_counter_instance = self.create_and_check_counter(
            TestCounterApi.source,
            SINGLE_FLAVORED_COUNTER_UNNAMED_DICT
        )
        counter_dict = unnamed_counter_instance.to_dict()
        print("Created counter: ", counter_dict)
        counter_dict.pop("metric_uuid")
        self.assertEqual(counter_dict, SINGLE_FLAVORED_COUNTER_UNNAMED_CREATED_DICT)

    def test_CounterSetters(self):
        """
        Test for using Counter class properties

        :rtype: void
        """
        period_value = 100
        flavor_value = RestResponse.ACCEPTED
        self.single_counter_instance.alerts = True
        self.single_counter_instance.period = period_value
        self.single_counter_instance.flavor = flavor_value
        self.assertTrue(self.single_counter_instance.alerts)
        self.assertIs(self.single_counter_instance.period, period_value)
        self.assertIs(self.single_counter_instance.flavor, flavor_value)

    def test_CounterCreationFail(self):
        """
        Test of failed creation of a counter

        :rtype: void
        """
        self.assertRaises(SyntaxError, CounterAPI.create_counter, TestCounterApi.source)

    def test_UpdateResetCounter_Fail(self):
        """
        Test of failed updating and resetting of a counter

        :rtype: void
        """
        self.assertFalse(CounterAPI.update_counter("not_real_uuid"))
        self.assertFalse(CounterAPI.reset_counter("not_real_uuid"))

    def test_CounterAccess(self):
        single_counter_dict = CounterAPI.get_counter(self.single_counter_instance.metric_uuid)
        single_counter_dict.pop("metric_uuid")
        self.assertEqual(
            single_counter_dict,
            SINGLE_COUNTER_CREATED_DETAILED_DICT
        )

    def test_DeleteFlavoredCounter(self):
        """
        Test deleting a flavored counter by flavor

        :rtype: void
        """
        CounterAPI.delete_flavored_counter(self.single_restresponse_counter_instance.flavor)
        self.assertFalse(CounterAPI.get_counter(
            self.single_restresponse_counter_instance.metric_uuid
        ))

    def test_FlavoredCounterAccess(self):
        """
        Test getting flavored counter when flavor is provided in string

        :rtype: void
        """
        restresponse_single_counter_dict = CounterAPI.get_flavored_counter_dict(
            FLAVOR_REST_RESPONSE_TYPE,
            FLAVOR_REST_RESPONSE_OPT
        )
        restresponse_single_counter_dict.pop("metric_uuid")
        self.assertEqual(restresponse_single_counter_dict, SINGLE_REST_RESPONSE_COUNTER_CREATED_DETAILED_DICT)

        not_created_flavor_opt = "RESET_CONTENT"
        flavored_single_counter_dict_empty = CounterAPI.get_flavored_counter_dict(
            FLAVOR_REST_RESPONSE_TYPE,
            not_created_flavor_opt
        )
        self.assertFalse(flavored_single_counter_dict_empty)

        restrequest_single_counter_dict = CounterAPI.get_flavored_counter_dict(
            FLAVOR_REST_REQUEST_TYPE,
            FLAVOR_REST_REQUEST_OPT
        )
        restrequest_single_counter_dict.pop("metric_uuid")
        self.assertEqual(restrequest_single_counter_dict, SINGLE_REST_REQUEST_COUNTER_CREATED_DETAILED_DICT)

        kwargs = {"flavor_type": "not_real_type", "flavor_opt": FLAVOR_REST_REQUEST_OPT}
        self.assertRaises(KeyError, CounterAPI.get_flavored_counter_dict, **kwargs)

    def test_FlavoredCounterAccess_Fail(self):
        """
        Test of failed access to a flavored counter

        :rtype: void
        """
        kwargs = {"flavor_type": FLAVOR_REST_RESPONSE_TYPE, "flavor_opt": "not_real_opt"}
        self.assertRaises(KeyError, CounterAPI.get_flavored_counter_dict, **kwargs)

    def test_GetAllCounters(self):
        """
        Test getting all counters summarized info

        :rtype: void
        """
        counters = CounterAPI.get_all_counters()
        counters_copy = counters
        for index, item in enumerate(counters_copy):
            counters[index].pop("metric_uuid")
        actual = sorted(counters, key=lambda k: k['name'])
        expected = sorted(MULTIPLE_COUNTERS_CREATED_LIST, key=lambda k: k['name'])
        self.assertEqual(expected, actual)

    def test_DeleteCounters(self):
        """
        Test deleting all counters and counters

        :rtype: void
        """
        CounterAPI.delete_counters()
        counters = CounterAPI.get_all_counters()
        self.assertFalse(counters)

    def test_DeleteCountersBySource(self):
        """
        Test deleting counters for a source

        :rtype: void
        """
        test_source = "test"
        self.create_and_check_counter(test_source, SINGLE_COUNTER_DICT)
        CounterAPI.delete_counters(test_source)
        self.test_GetAllCounters()

    def test_GetFlavoredCounters(self):
        """
        Test getting flavored counter

        :rtype: void
        """
        counters = CounterAPI.get_flavored_counters(FLAVOR_REST_REQUEST_TYPE)
        self.assertEqual(len(counters), 1)
        counter_dict = counters[0]
        counter_dict.pop("metric_uuid")
        self.assertEqual(counter_dict, SINGLE_REST_REQUEST_COUNTER_CREATED_DICT)

    def test_CreateFlavoredCounterFromStr(self):
        """
        Creates a flavored counter from a flavor_string

        :rtype: void
        """
        flavor_opt = "Delete"
        success, metric_uuid = CounterAPI.create_flavored_counter(
            FLAVOR_REST_REQUEST_TYPE,
            TestCounterApi.source,
            flavor_opt,
            **SINGLE_COUNTER_DICT
        )
        self.assertTrue(success)
        self.assertIsNotNone(metric_uuid)

        kwargs = {
            "flavor_type": "not_real_flavor",
            "source": TestCounterApi.source,
            "flavor_opt": flavor_opt,
            "counter_dict": SINGLE_COUNTER_DICT
        }

        self.assertRaises(KeyError, CounterAPI.create_flavored_counter, **kwargs)

        kwargs["flavor_type"] = FLAVOR_REST_REQUEST_TYPE
        kwargs["flavor_opt"] = "not_real_opt"

        self.assertRaises(KeyError, CounterAPI.create_flavored_counter, **kwargs)

    def test_FlavorStrToInstance_Fail(self):
        """
        Transfers Flavor string to Enum instance and checks it

        :rtype: void
        """
        flavor_kwargs = {
            "flavor_type": "test",
            "flavor_opt": FLAVOR_REST_REQUEST_OPT
        }

        self.assertRaises(KeyError, lambda: flavor_str_to_instance(**flavor_kwargs))
