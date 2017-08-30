#! /usr/bin/python3

from magen_statistics_api.counter_metric import Counter
from magen_statistics_api.metric import MetricsCollections
from magen_statistics_api.metric_flavors import RestResponse, RestRequest

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"

metrics_collections = MetricsCollections()


def get_counter_instance(counter_uuid):
    return metrics_collections.get_metric_by_uuid(Counter.__name__, counter_uuid)


def get_flavored_counter_instance(flavor):
    return metrics_collections.get_metric_by_flavor(Counter.__name__, flavor)


def flavor_str_to_instance(flavor_type, flavor_opt):
    if flavor_type.lower() == RestResponse.__name__.lower():
        return vars(RestResponse)[flavor_opt.upper()]
    elif flavor_type.lower() == RestRequest.__name__.lower():
        return vars(RestRequest)[flavor_opt.upper()]
    else:
        raise KeyError("flavor_type or flavor_opt do not exist")


def assign_flavor(flavor_type, flavor_opt, counter_dict):
    """
    Function assigning flavors to counter_dict based on

    :param counter_dict: dictionary with counter data
    :param flavor_opt: flavor option
    :param flavor_type: type of flavor; usually name of class
    :return: modified counter_dict
    :rtype: dict
    """
    counter_dict["flavor"] = flavor_str_to_instance(flavor_type, flavor_opt)
    return counter_dict


class CounterAPI(object):

    @staticmethod
    def create_counter(source, **kwargs):
        """
        API method to create a Counter metric

        :param source: string, name of service invoked counter creation
        :param kwargs: dict, all metric parameters that are optional for counter creation
        :return: uuid of the Counter object
        :rtype: uuid string
        """
        flavor_value = kwargs.get("flavor", None)
        if flavor_value:
            flavor_list = flavor_value.split(".")
            kwargs = assign_flavor(flavor_list[0], flavor_list[1], kwargs)
        counter = Counter(source, **kwargs)
        return counter.uuid

    @staticmethod
    def update_counter(counter_uuid, value=0):
        """
        API method to update value of the Counter metric

        :param counter_uuid: string
        :param value: int, value to add to counter
        :rtype: void
        """
        counter = get_counter_instance(counter_uuid)
        if counter:
            counter.increment(value)
            return True
        else:
            return False

    @staticmethod
    def reset_counter(counter_uuid):
        """
        API method to reset Counter metric by setting it's value to 0 and clearing DB history

        :param counter_uuid: string
        :rtype: void
        """
        counter = get_counter_instance(counter_uuid)
        if counter:
            counter.reset()
            return True
        else:
            return False

    @staticmethod
    def delete_counter(counter_uuid):
        """
        API method to remove Counter metric from the system and DB

        :param counter_uuid: string
        :rtype: void
        """
        metrics_collections.remove_metric_by_uuid(Counter.__name__, counter_uuid)

    @staticmethod
    def delete_flavored_counter(flavor):
        metrics_collections.remove_metric_by_flavor(Counter.__name__, flavor)

    @staticmethod
    def get_counter(counter_uuid):
        counter = get_counter_instance(counter_uuid)
        if counter:
            counter.provide_detailed_info = True
            return counter.to_dict()
        else:
            return dict()

    @staticmethod
    def get_flavored_counter_dict(flavor_type, flavor_opt):
        flavor = flavor_str_to_instance(flavor_type, flavor_opt)
        counter = get_flavored_counter_instance(flavor)
        if counter:
            counter.provide_detailed_info = True
            return counter.to_dict()
        else:
            return dict()

    @staticmethod
    def get_all_counters():
        """
        API method to get all available counters in the system

        :return: list of counters
        :rtype: list
        """
        counters = metrics_collections.get_collection(Counter.__name__)
        counters_list = []
        if counters:
            for counter in counters.values():
                counter.provide_detailed_info = False
                counters_list.append(counter.to_dict())
        return counters_list

    @staticmethod
    def delete_counters(source=None):
        """
        API method to delete all counters in the system

        :rtype: void
        """
        if source:
            metrics_collections.remove_metrics_for_source(Counter.__name__, source)
        else:
            metrics_collections.del_collection(Counter.__name__)

    @staticmethod
    def get_counters_by_source(source):
        """
        API method to get all counters belong to the same source

        :param source: string; name of the service that invoked counter creation
        :return: list of counters
        :rtype: list
        """
        counters = metrics_collections.get_collection(Counter.__name__)
        counter_list = []
        if counters:
            for counter in counters.values():
                counter.provide_detailed_info = False
                if counter.source.lower() == source.lower():
                    counter_list.append(counter.to_dict())
        return counter_list

    @staticmethod
    def get_flavored_counters(flavor_type_string, source=None):
        """
        API method to get flavored counters to the same source if provided

        :param flavor_type_string: name of flavor
        :param source: name of source
        :return: list of counters
        :rtype: list
        """
        # flavor = flavor_str_to_instance()
        counters = metrics_collections.get_collection(Counter.__name__)
        result_list = []
        if not counters:
            return result_list
        for counter in counters.values():
            counter.provide_detailed_info = False
            if not source or counter.source.lower() == source.lower():
                if counter.flavor and counter.flavor.flavor_name.lower() == flavor_type_string.lower():
                    result_list.append(counter.to_dict())
        return result_list

    @staticmethod
    def create_flavored_counter(flavor_type, source, flavor_opt, **counter_dict):
        """
        API method to create flavored counter for a given source.

        :param counter_dict: dictionary with counter data
        :param flavor_opt: flavor option
        :param flavor_type: type of flavor; usually name of class
        :param source: name of the source invoked counter creation
        :rtype: void
        """
        counter_dict = assign_flavor(flavor_type, flavor_opt, counter_dict)
        counter = Counter(source, **counter_dict)
        return True, counter.uuid
