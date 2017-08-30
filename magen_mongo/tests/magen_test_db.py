import os
from pymongo import MongoClient

from magen_datastore_apis.main_db import MainDb

#
# Copyright (c) 2015 Cisco Systems, Inc. and others.  All rights reserved.
#

__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

MONGO_PORT = 27017


class MagenTestDb(MainDb):

    __instance = None

    def __init__(self):
        super().__init__()
        try:
            mongo_ip_port = os.environ["MONGO_IP_PORT"]
            mongo_ip = mongo_ip_port.split(":")[0]
            mongo_locator = "{ip}:{port}".format(ip=mongo_ip, port=MONGO_PORT)
        except KeyError:
            mongo_locator = "{ip}:{port}".format(ip='127.0.0.1', port=MONGO_PORT)
            print("Using local Mongo")
        self.__db_ip_port = mongo_locator
        self.__mongo_client = MongoClient(self.db_ip_port)
        self.__magen_test_db = self.__mongo_client.get_database('magen_test')
        self.__magen_test_collection = self.__magen_test_db.get_collection('magen_test_collection')

    @property
    def db_ip_port(self):
        """DB Element Strategy"""
        return self.__db_ip_port

    @db_ip_port.setter
    def db_ip_port(self, value):
        self.__db_ip_port = value

    @property
    def mongo_client(self):
        return self.__mongo_client

    @mongo_client.setter
    def mongo_client(self, value):
        self.__mongo_client = value

    @property
    def magen_test_db(self):
        return self.__magen_test_db

    @magen_test_db.setter
    def magen_test_db(self, value):
        self.__magen_test_db = value

    @property
    def magen_test_collection(self):
        return self.__magen_test_collection

    @magen_test_collection.setter
    def magen_test_collection(self, value):
        self.__magen_test_collection = value

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


