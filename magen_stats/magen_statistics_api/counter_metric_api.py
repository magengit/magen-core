#! /usr/bin/python3
"""Counter Metric API"""

from magen_statistics_api.counter_metric import Counter
from magen_statistics_api.metric import MetricsCollections
from magen_statistics_api.metric_flavors import RestResponse, RestRequest

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "09/23/2017"

METRICS_COLLECTIONS = MetricsCollections()


def get_counter_instance(counter_uuid):
    """
    Get Counter instantiated object by UUID provided

    :param counter_uuid: Counter unique ID
    :type counter_uuid: uuid str
    """
    return METRICS_COLLECTIONS.get_metric_by_uuid(Counter.__name__, counter_uuid)


def get_flavored_counter_instance(flavor):
    """
    Get Flavored Counter instantiated object by flavor name provided

    :param flavor: Flavor class (RestRequest|RestResponse)
    :type flavor: str

    :return: Counter object
    """
    return METRICS_COLLECTIONS.get_metric_by_flavor(Counter.__name__, flavor)


def flavor_str_to_instance(flavor_type, flavor_opt):
    """
    Cast flavor_type and flavor_opt strings to objects

    :param flavor_type: Flavor class (RestRequest|RestResponse)
    :type flavor_type: str
    :param flavor_opt: Flavor option (GET|POST|DELETE|PUT --> for RestRequest)
                                     (HTTPStatus options --> for RestResponse)

    :type flavor_opt: str

    :return: RestResponse or RestRequest class object
    :rtype: object
    """
    if flavor_type.lower() == RestResponse.__name__.lower():
        return vars(RestResponse)[flavor_opt.upper()]
    elif flavor_type.lower() == RestRequest.__name__.lower():
        return vars(RestRequest)[flavor_opt.upper()]
    else:
        raise KeyError("flavor_type: {} or flavor_opt: {} do not exist".format(flavor_type, flavor_opt))


def assign_flavor(flavor_type, flavor_opt, counter_dict):
    """
    Function assigning flavors to counter_dict based on

    :param counter_dict: dictionary with counter data
    :type counter_dict: dict
    :param flavor_type: Flavor class (RestRequest|RestResponse)
    :type flavor_type: str
    :param flavor_opt: Flavor option (GET|POST|DELETE|PUT --> for RestRequest)
                                     (HTTPStatus options --> for RestResponse)

    :type flavor_opt: str

    :return: modified counter_dict
    :rtype: dict
    """
    counter_dict["flavor"] = flavor_str_to_instance(flavor_type, flavor_opt)
    return counter_dict


class CounterAPI(object):
    """Counter API. CRUD operations"""

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
        return counter.metric_uuid

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
        return False

    @staticmethod
    def delete_counter(counter_uuid):
        """
        API method to remove Counter metric from the system and DB

        :param counter_uuid: Counter unique id
        :type counter_uuid: uuid str

        :rtype: void
        """
        METRICS_COLLECTIONS.remove_metric_by_uuid(Counter.__name__, counter_uuid)

    @staticmethod
    def delete_flavored_counter(flavor):
        """
        Delete Flavored Counter by flavor name

        :param flavor: Counter Flavor like RestResponse or RestRequest
        :type flavor: str

        rtype: void
        """
        METRICS_COLLECTIONS.remove_metric_by_flavor(Counter.__name__, flavor)

    @staticmethod
    def get_counter(counter_uuid):
        """
        Request Counter instance from Metrics Collections

        :param counter_uuid: Counter unique id
        :type counter_uuid: uuid str

        :return: Counter details
        :rtype: dict
        """
        counter = get_counter_instance(counter_uuid)
        if counter:
            counter.provide_detailed_info = True
            return counter.to_dict()
        return dict()

    @staticmethod
    def get_flavored_counter_dict(flavor_type, flavor_opt):
        """
        Request Flavored Counter by flavor from Metrics collections

        :param flavor_type: Flavor class (RestRequest|RestResponse)
        :type flavor_type: str
        :param flavor_opt: Flavor option (GET|POST|DELETE|PUT --> for RestRequest)
                                         (HTTPStatus options --> for RestResponse)
        :type flavor_opt: str
        """
        flavor = flavor_str_to_instance(flavor_type, flavor_opt)
        counter = get_flavored_counter_instance(flavor)
        if counter:
            counter.provide_detailed_info = True
            return counter.to_dict()
        return dict()

    @staticmethod
    def get_all_counters():
        """
        API method to get all available counters in the system

        :return: list of counters
        :rtype: list
        """
        counters = METRICS_COLLECTIONS.get_collection(Counter.__name__)
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
            METRICS_COLLECTIONS.remove_metrics_for_source(Counter.__name__, source)
            return
        METRICS_COLLECTIONS.del_collection(Counter.__name__)

    @staticmethod
    def get_counters_by_source(source):
        """
        API method to get all counters belong to the same source

        :param source: name of the service that invoked counter creation
        :type source: string

        :return: list of counters
        :rtype: list
        """
        counters = METRICS_COLLECTIONS.get_collection(Counter.__name__)
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
        counters = METRICS_COLLECTIONS.get_collection(Counter.__name__)
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
        return True, counter.metric_uuid
