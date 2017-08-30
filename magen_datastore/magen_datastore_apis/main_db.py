from abc import ABCMeta

#
# Copyright (c) 2015 Cisco Systems, Inc. and others.  All rights reserved.
#


__author__ = "rpenno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class MainDb (metaclass=ABCMeta):
    """
    Strategy for Main Database Singleton
    """

    __instance = None

    def __init__(self):

        super().__init__()
        self.__core_database = None

    @classmethod
    def get_instance(cls):
        if MainDb.__instance is None:
            MainDb.__instance = cls()
        return MainDb.__instance

    @staticmethod
    def get_core_db_instance():
        return MainDb.get_instance().core_database

    @staticmethod
    def get_analytics_db_instance():
        return MainDb.get_instance().analytics_database

    @property
    def core_database(self):
        """DB Element Strategy"""
        return self.__core_database

    @core_database.setter
    def core_database(self, value):
        self.__core_database = value

    def initialize(self):
        pass
