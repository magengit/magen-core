"""Abstract Class for Main Magen Database"""
from abc import ABCMeta

__author__ = "rpenno"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class MainDb(metaclass=ABCMeta):
    """
    Strategy for Main Database Singleton
    """

    __instance = None

    def __init__(self):

        super().__init__()
        self.__core_database = None

    @classmethod
    def get_instance(cls):
        """Main Singleton method to get instance"""
        if MainDb.__instance is None:
            MainDb.__instance = cls()
        return MainDb.__instance

    @staticmethod
    def get_core_db_instance():
        """
        MainDb implements a strategy pattern. MainDb registers core database to provide easy access
        """
        return MainDb.get_instance().core_database

    @property
    def core_database(self):
        """DB Element Strategy"""
        return self.__core_database

    @core_database.setter
    def core_database(self, value):
        self.__core_database = value

    def initialize(self):
        """Initialize actual DB instance"""
        pass
