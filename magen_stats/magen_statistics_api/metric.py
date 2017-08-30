#! /usr/bin/python3

from magen_utils_apis.parse_utils import replace_keys
from magen_utils_apis.singleton_meta import Singleton

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"


class Metric(object):
    """
        This class describes a Metric base for statistics item of Magen.
        Properties of this class are aggregated information that each type of Metrics must have
        optional properties: frequency and abs_value
    """

    def __init__(self, name, source, abs_value=0):
        """
        This method initializes all properties of Metrics class and get instance of MetricsCollection Singleton

        :param name: any string without spaces; name of Metric
        :param source: string; name of Service that invoked Metric creation
        :param abs_value: positive integer; value of the metric upon creation, default = 0
        """
        self.__name = name
        self.__source = source
        self.__abs_value = abs_value
        self.__namespace = __class__.__name__
        self.__uuid = None
        self.__provide_detailed_info = False
        self.__metrics_collections = MetricsCollections()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, new_source):
        self.__source = new_source

    @property
    def abs_value(self):
        return self.__abs_value

    @abs_value.setter
    def abs_value(self, new_abs_value):
        self.__abs_value = new_abs_value

    @property
    def namespace(self):
        return self.__namespace

    @namespace.setter
    def namespace(self, new_entity):
        self.__namespace = self.__namespace + "." + new_entity

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, value):
        self.__uuid = value

    @property
    def provide_detailed_info(self):
        return self.__provide_detailed_info

    @provide_detailed_info.setter
    def provide_detailed_info(self, value):
        self.__provide_detailed_info = value

    @property
    def metrics_collections(self):
        return self.__metrics_collections

    @metrics_collections.setter
    def metrics_collections(self, value):
        self.__metrics_collections = value

    def to_dict(self):
        properties = vars(self)
        pattern = '_' + __class__.__name__ + '__'
        split_str = "__"
        include_keys = []  # by default all keys are included
        if not self.provide_detailed_info:
            include_keys.append("uuid")
            include_keys.append("name")
            include_keys.append("abs_value")
        return replace_keys(properties, pattern, split_str, include_keys)


class MetricsCollections(metaclass=Singleton):
    """
    This class represents a Singleton that collects all Metrics instances of different types that had been created
    """

    def __init__(self):
        """
        collections is a property that collects a dictionary of different types of Metrics and lists of invoked items
        """
        self.__collections = dict()

    @property
    def collections(self):
        return self.__collections

    @collections.setter
    def collections(self, value):
        self.__collections = value

    def add_to_collection(self, collection_name, metric_instance):
        """
        Adds new collection to collections property and creates and empty list.
        Duplicates are stored only for internal access

        :param collection_name: name of Metrics collection
        :param metric_instance: instance of class type of Metric (Counter, Gauge etc.)
        :rtype: void
        """
        # stack = inspect.stack()
        # class_caller_name = stack[1][0].f_locals["self"].__class__.__name__
        if collection_name not in self.__collections.keys():
            self.__collections[collection_name] = dict()
        if metric_instance.flavor:
            # FIXME: have to store duplicates in order to provide easy access and full functionality for API
            self.__collections[collection_name][metric_instance.flavor] = metric_instance
            self.__collections[collection_name][metric_instance.uuid] = metric_instance
        else:
            self.__collections[collection_name][metric_instance.uuid] = metric_instance

    def get_collection(self, name):
        """
        Returns collection that contains only unique items

        :param name: collection name
        :rtype: dictionary
        """
        collection = self.__collections.get(name, None)
        result_dict = dict()
        if collection:
            for metric in collection.keys():
                if isinstance(metric, str):
                    result_dict[metric] = collection[metric]
        return result_dict

    def del_collection(self, name):
        try:
            del self.__collections[name]
        except KeyError:
            pass

    def get_metric_by_uuid(self, metric_type: str, uuid: str):
        collection = self.__collections.get(metric_type, None)
        if collection:
            return collection.get(uuid, None)
        return None

    def get_metric_by_flavor(self, metric_type, flavor):
        collection = self.__collections.get(metric_type, None)
        if collection:
            return collection.get(flavor, None)
        return None

    def remove_metric_by_uuid(self, metric_type, uuid):
        collection = self.__collections.get(metric_type, None)
        if collection:
            try:
                metric = collection[uuid]
                try:
                    del collection[metric.flavor]
                except KeyError:
                    pass
                del collection[uuid]
            except KeyError:
                pass

    def remove_metric_by_flavor(self, metric_type, flavor):
        collection = self.__collections.get(metric_type, None)
        if collection:
            try:
                metric = collection[flavor]
                del collection[metric.uuid]
                del collection[flavor]
            except KeyError:
                pass

    def remove_metrics_for_source(self, metric_type, source_name):
        collection = self.__collections.get(metric_type, None)
        if collection:
            uuid_keys = [k for k, v in collection.items() if v.source.lower() == source_name.lower()]
            for uuid in uuid_keys:
                try:
                    del collection[uuid]
                except KeyError:
                    pass

    def clear(self):
        self.__collections.clear()
