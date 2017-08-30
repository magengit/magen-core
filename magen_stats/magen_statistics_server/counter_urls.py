#! /usr/bin/python3
from magen_rest_apis.magen_urls import MagenUrls

__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__email__ = "alifar@cisco.com"
__date__ = "10/24/2016"


class CounterUrls(MagenUrls):
    """
    This class provides bases for Counters URLs
    Inherits from MagenUrls class
    """

    def __init__(self, source_server, source_name):
        super().__init__()
        base = self.http_base+source_server+"/magen/"+source_name
        counters = "/v2/counters/"
        self.__counters_url = base+counters
        self.__restresponse_counters_url = base+counters+"restresponse/"
        self.__restresponse_ok_counter_url = base+counters+"restresponse/"+"ok/"
        self.__restrequest_counters_url = base+counters+"restrequest/"
        self.__restrequest_get_counter_url = base+counters+"restrequest/"+"get/"
        self.__restresponse_counter_template_url = base+counters+"restresponse/{}"
        self.__restrequest_counter_template_url = base+counters+"restrequest/{}"

    @property
    def counters_url(self):
        return self.__counters_url

    @counters_url.setter
    def counters_url(self, value):
        pass

    @property
    def restresponse_counters_url(self):
        return self.__restresponse_counters_url

    @restresponse_counters_url.setter
    def restresponse_counters_url(self, value):
        pass

    @property
    def restresponse_ok_counter_url(self):
        return self.__restresponse_ok_counter_url

    @restresponse_ok_counter_url.setter
    def restresponse_ok_counter_url(self, value):
        pass

    @property
    def restrequest_counters_url(self):
        return self.__restrequest_counters_url

    @restrequest_counters_url.setter
    def restrequest_counters_url(self, value):
        pass

    @property
    def restrequest_get_counter_url(self):
        return self.__restrequest_get_counter_url

    @restrequest_get_counter_url.setter
    def restrequest_get_counter_url(self, value):
        pass

    @property
    def restresponse_counter_template_url(self):
        return self.__restresponse_counter_template_url

    @restresponse_counter_template_url.setter
    def restresponse_counter_template_url(self, value):
        pass

    @property
    def restrequest_counter_template_url(self):
        return self.__restrequest_counter_template_url

    @restrequest_counter_template_url.setter
    def restrequest_counter_template_url(self, value):
        pass

    def get_urls(self):
        return {
            "counters_url": self.counters_url,
            "restresponse_counters_url": self.restresponse_counters_url,
            "restrequest_counters_url": self.restrequest_counters_url,
            "restresponse_counter_url": self.restresponse_counter_template_url,
            "restrequest_counter_url": self.restrequest_counter_template_url
        }
