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
        pass

    @abstractmethod
    def add_to_set(self, dict_seed, action_dict):
        pass

    @abstractmethod
    def delete(self, seed):
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def select_all(self):
        pass

    @abstractmethod
    def select_by_condition(self, seed):
        pass

    @abstractmethod
    def initialize_bulk_operation(self):
        pass

    @abstractmethod
    def execute_bulk_operation(self, bulk_obj):
        pass

    @abstractmethod
    def bulk_insert(self, bulk_obj, data):
        pass

    @abstractmethod
    def bulk_remove_one(self, bulk_obj, uuid):
        pass

    @abstractmethod
    def insert_many(self, data_list):
        pass

    @abstractmethod
    def find_one_filter(self, seed):
        pass

    @abstractmethod
    def bulk_add_to_set(self, bulk_obj, dict_seed, action_dict):
        pass
