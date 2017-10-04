#! /usr/bin/python3

import unittest
from unittest.mock import Mock, patch

import logging

import magen_core_test_env
from magen_utils_apis.dd_events_wrapper import EventsSubmitError
from magen_utils_apis.dd_events_wrapper import DDEventsWrapper

__author__ = "Alena Lifar"
__email__ = "alifar_at_cisco.com"
__version__ = "0.1"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__status__ = "alpha"


class EventsCtrlTest(unittest.TestCase):
    _events_ctrl = None
    _app_name = "TEST"
    _abs_patch = None
    _logger = logging.getLogger('events_tests')

    @classmethod
    def setUpClass(cls):
        cls._abs_patch = patch.multiple(DDEventsWrapper, __abstractmethods__=set())
        cls._abs_patch.start()
        cls._events_ctrl = DDEventsWrapper(application_name=cls._app_name, magen_logger=cls._logger)

    @classmethod
    def tearDownClass(cls):
        cls._abs_patch.stop()

    def test_DefaultTagging(self):
        """
        This method checks that default tags are getting constructed
        and assigned to a cls variable
        if proper initializing was done
        :return: void
        """
        print()
        print("======= Default Tagging Test =======")
        test_tags = DDEventsWrapper.default_tags()
        print(test_tags)
        self.assertIsInstance(test_tags, list)
        self.assertEquals(test_tags, DDEventsWrapper.tags())

    def test_UpdateTags(self):
        """
        This method checks adding a new tag and makes sure default tags remain the same
        :return: void
        """
        print()
        print("======= Update Tags Test =======")
        update_tag = "mode:test"
        DDEventsWrapper.update_tags(update_tag)
        test_tags = DDEventsWrapper.tags()
        print("Updated Tags: ", test_tags)
        print("Default Tags: ", DDEventsWrapper.default_tags())
        self.assertIn(update_tag, test_tags)
        self.assertNotEqual(test_tags, DDEventsWrapper.default_tags())
        self.assertEquals(len(DDEventsWrapper.default_tags()), DDEventsWrapper.num_default_tags)

    def test_UpdateTagsFail(self):
        """
        This method checks that proper exception is thrown if malformed tag provided
        :return: void
        """
        print()
        print("======= Update Tags Fail Test =======")
        update_tag_malformed = "test-mode"
        with self.assertRaises(SyntaxError) as context:
            DDEventsWrapper.update_tags(update_tag_malformed)
        print(context.exception.msg)
        self.assertEquals('tag must be of format <str>:<str>', context.exception.msg)

    def test_SendEvent(self):
        """
        This method checks that correctly formed event gets sent and id is added to a collection
        :return: void
        """
        test_id1 = 123
        mock_response1 = Mock()
        mock_response1.return_value = {"status": "ok", "event": {"id": test_id1}}
        with patch('datadog.api.Event.create', new=mock_response1):
            EventsCtrlTest._events_ctrl.send_event("test", "test")

        test_id2 = 321
        mock_response2 = Mock()
        mock_response2.return_value = {"status": "ok", "event": {"id": test_id2}}
        with patch('datadog.api.Event.create', new=mock_response2):
            EventsCtrlTest._events_ctrl.send_event("test", "test")

        self.assertIn(test_id1, EventsCtrlTest._events_ctrl.event_id_collection)
        self.assertIn(test_id2, EventsCtrlTest._events_ctrl.event_id_collection)

    def test_SendEventFail(self):
        """
        This method checks if event was not added to Datadog an exception is thrown
        :return: void
        """
        print()
        print("======= Send Event Fail Test =======")
        mock_response = Mock()
        mock_response.return_value = {"status": "fail"}
        with patch('datadog.api.Event.create', new=mock_response):
            with self.assertRaises(EventsSubmitError) as context:
                EventsCtrlTest._events_ctrl.send_event("test", None)

        print(context.exception.msg)
        self.assertIn("Event creation error", context.exception.msg)

    def test_ProhibitedSetters(self):
        """
        This method checks properties prohibited from setting
        :return: void
        """
        print()
        print("======= Prohibited Setters Test =======")
        EventsCtrlTest._events_ctrl.event_id_collection.append("test")
        check_value = EventsCtrlTest._events_ctrl.event_id_collection
        EventsCtrlTest._events_ctrl.event_id_collection = ["this value will not be set"]
        self.assertEquals(EventsCtrlTest._events_ctrl.event_id_collection, check_value)

    def test_CleanUp(self):
        """
        This method creates an event and pushes it to Datadog then deletes it using stored id in event_id_collection
        :return: void
        """
        print()
        print("======= Clean Up Test =======")
        test_id = 123
        mock_response = Mock()
        mock_response.return_value = {"status": "ok", "event": {"id": test_id}}
        with patch('datadog.api.Event.create', new=mock_response):
            EventsCtrlTest._events_ctrl.send_event("test", "test")
        self.assertEquals(EventsCtrlTest._events_ctrl.event_id_collection[0], test_id)
        with patch('datadog.api.Event.delete'):
            EventsCtrlTest._events_ctrl.clean_up()
        self.assertEquals(EventsCtrlTest._events_ctrl.event_id_collection, list())
