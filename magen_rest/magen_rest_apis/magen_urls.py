#! /usr/bin/python3
"""Magen Urls class stores known headers for requests handling"""
from magen_utils_apis.singleton_meta import Singleton

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"


class MagenUrls(metaclass=Singleton):
    """Known Headers for Magen App"""
    def __init__(self):
        self.__put_json_headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        self.__get_json_headers = {'Accept': 'application/json'}

        self.__post_xml_headers = {'content-type': 'application/xml', 'Accept': 'application/xml'}
        self.__get_xml_headers = {'Accept': 'application/xml'}
        self.http_base = "http://"

    @property
    def put_json_headers(self):
        """PUT JSON Headers"""
        return self.__put_json_headers

    @put_json_headers.setter
    def put_json_headers(self, value):
        pass

    @property
    def get_json_headers(self):
        """GET JSON Headers"""
        return self.__get_json_headers

    @get_json_headers.setter
    def get_json_headers(self, value):
        pass

    @property
    def post_xml_headers(self):
        """POST XML Headers"""
        return self.__post_xml_headers

    @post_xml_headers.setter
    def post_xml_headers(self, value):
        pass

    @property
    def get_xml_headers(self):
        """GET XML Headers"""
        return self.__get_xml_headers

    @get_xml_headers.setter
    def get_xml_headers(self, value):
        self.__get_xml_headers = value
