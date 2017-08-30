#! /usr/bin/python3

from flask import Flask
from flask_cors import CORS
from magen_rest_apis.magen_app import CustomJSONEncoder
from magen_utils_apis.magen_flask_response import JSONifiedResponse
from magen_utils_apis.singleton_meta import Singleton

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"


class MetricsApp(metaclass=Singleton):

    # __metrics = None

    def __init__(self):
        _MetricsFlask = type('MetricsFlask', (Flask,), {'response_class': JSONifiedResponse})
        self.__metrics = _MetricsFlask(__name__)
        self.__metrics.json_encoder = CustomJSONEncoder
        CORS(self.__metrics)

    @property
    def metrics(self):
        return self.__metrics

    @metrics.setter
    def metrics(self, value):
        pass
