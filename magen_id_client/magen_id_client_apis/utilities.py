"""Utilities functools for Magen Client"""
import uuid

from urllib.parse import urlparse

__author__ = "michowdh@cisco.com"
__maintainer__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


def get_the_encoded_url(str_url):
    """
    This function encodes the url

    :param str_url: url string
    :return: encoded url string
    :rtype: string
    """
    url_object = urlparse(str_url)
    return url_object.geturl()


def randomstr(str_length=40):
    """
    This function creates random string

    :param str_length: the length of random string
    :return: random string
    :rtype: string
    """
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-", "")
    return random[0:str_length]
