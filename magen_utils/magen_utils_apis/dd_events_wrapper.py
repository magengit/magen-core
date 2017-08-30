#! /usr/bin/python3
from abc import ABCMeta, abstractmethod

import datadog
from datadog.api.exceptions import ApiNotInitialized
import json

from magen_rest_apis.server_urls import ServerUrls

__author__ = "Alena Lifar"
__email__ = "alifar@cisco.com"
__version__ = "0.1"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__status__ = "alpha"


T_FEAT = "events_dev"  # feature tag


class EventsSubmitError(Exception):
    def __init__(self, message):
        super(EventsSubmitError, self).__init__(message)
        self.__msg = message

    @property
    def msg(self):
        return self.__msg


class DDEventsWrapper(metaclass=ABCMeta):
    """
    This is a base class for Event controlling
    """
    _tags = None  # tags collection
    app_tag = None  # application tag that is initialized on __init__: <str>
    server_urls = ServerUrls.get_instance()
    num_default_tags = 3

    def __init__(self, application_name: str, magen_logger):
        """
        Configures Datadog API with given keys

        :param application_name: string
        """
        self.logger = magen_logger
        self.dd = datadog.api.Event

        DDEventsWrapper.app_tag = application_name

        try:
            datadog.initialize()
            self.dd.create(
                title="Initialization DD",
                text="Initialization is successful",
                alert_type='success',
                tags=DDEventsWrapper.tags()
            )
        except ApiNotInitialized:
            self.logger.error('DATADOG initialization failed! Events will not be sent')
            pass

        self.__event_id_collection = list()

    @property
    def event_id_collection(self):
        return self.__event_id_collection

    @event_id_collection.setter
    def event_id_collection(self, value):
        pass

    @classmethod
    def default_tags(cls):
        """
        Returns default tags that gets constructed on the first call to this method

        :return: list of tags
        """
        if cls._tags:
            return cls._tags[:cls.num_default_tags]
        cls._tags = list()
        cls._tags.append(
            "feature:{}".format(T_FEAT)
        )
        cls._tags.append(
            "application:{}".format(cls.app_tag)
        )
        cls._tags.append(
            "domain:{}".format(cls.server_urls.domain_name)
        )
        return cls._tags

    @classmethod
    def update_tags(cls, *args):
        """
        Add a new tag to a tags collection

        :rtype: void
        """
        for tag in args:
            if ":" not in tag:
                raise SyntaxError("tag must be of format <str>:<str>")
            cls._tags.append(tag)

    @classmethod
    def tags(cls):
        return cls._tags if cls._tags else cls.default_tags()

    def send_event(self, event_name: str, event_data: dict, alert=None, default_tags=False):
        """

        Wrapper to a DD event create method

        :param event_name: title of the Event
        :param event_data: dictionary of the Event data
        :param alert: 'success', 'warning' or 'error' - str
        :param default_tags: boolean to invoke providing only default tags
        :return: created event
        :rtype: dict

        """
        try:
            dd_event = self.dd.create(
                title=event_name,
                text=json.dumps(event_data),
                alert_type=alert,
                tags=DDEventsWrapper.tags() if not default_tags else DDEventsWrapper.default_tags()
            )
            if dd_event['status'] == 'ok':
                self.event_id_collection.append(dd_event['event']['id'])
            else:
                raise EventsSubmitError("Event creation error: {}".format(dd_event))
            return dd_event
        except ApiNotInitialized:
            pass

    def clean_up(self):
        """
        Removes all created events in current session using event_id_collection property

        :rtype: void
        """
        if self.event_id_collection:
            for item in self.event_id_collection:
                self.dd.delete(item)
        self.event_id_collection.clear()

    @classmethod
    @abstractmethod
    def construct_event(cls, validation_data, **kwargs):
        pass


