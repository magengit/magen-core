import uuid

from urllib.parse import urlparse

__author__ = "michowdh@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class Utilities(object):
    @staticmethod
    def get_the_encoded_url(str_url):
        """
        This function encodes the url

        :param str_url: url string
        :return: encoded url string
        :rtype: string
        """
        o = urlparse(str_url)
        return o.geturl()

    @staticmethod
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
