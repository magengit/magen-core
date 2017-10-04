"""Interface for Magen Datastore API"""
from abc import ABCMeta, abstractmethod

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class IDao(metaclass=ABCMeta):
    """
    This class is abstract strategy
    that will be implemented with default implementation.
    This will allow to have less repeated code
    """

    @abstractmethod
    def insert(self, data, additional_data=None):
        """
        Insert Abstract Method
        :param data: data to insert
        :data type: Iterable
        :param additional_data: other meta data
        """
        pass

    @abstractmethod
    def add_to_set(self, dict_seed, action_dict):
        """
        Add To Set Abstract Method
        :param dict_seed: filter to find set
        :param action_dict: action with found set
        """
        pass

    @abstractmethod
    def delete(self, seed):
        """
        Delete Abstract Method
        :param seed: filter to find record
        """
        pass

    @abstractmethod
    def delete_all(self):
        """Delete All Abstract Method"""
        pass

    @abstractmethod
    def select_all(self, projection=None):
        """
        Select All Abstract Method
        :param projection: optional filter
        """
        pass

    @abstractmethod
    def select_by_condition(self, seed, projection=None):
        """
        Select By Condition Abstract Method
        :param seed: filter condition
        :param projection: Other optional filters
        """
        pass

    @abstractmethod
    def initialize_bulk_operation(self):
        """Initialize Bulk Operation Abstract Method"""
        pass

    @abstractmethod
    def execute_bulk_operation(self, bulk_obj):
        """
        Execute Bulk Operaction Abstract Method
        :param bulk_obj: Bulk Object
        """
        pass

    @abstractmethod
    def bulk_insert(self, bulk_obj, data):
        """
        Bulk Insert Abstract Method
        :param bulk_obj: Bulk object
        :param data: data to be inserted
        """
        pass

    @abstractmethod
    def bulk_remove_one(self, bulk_obj, uuid):
        """Bulk Remove One Abstract Method"""
        pass

    @abstractmethod
    def insert_many(self, data_list):
        """
        Insert Many Abstract Method
        :param data_list: data to be inserted
        """
        pass

    @abstractmethod
    def find_one_filter(self, seed, projection=None):
        """
        Find One using filter Abstract Method
        :param seed: filter
        :param projection: optional filter
        """
        pass

    @abstractmethod
    def bulk_add_to_set(self, bulk_obj, dict_seed, action_dict):
        """
        Bulk Add To Set Abstract Method
        :param bulk_obj: Bulk object
        :param dict_seed: filter to find set
        :param action_dict: action to perform on found set
        """
        pass
