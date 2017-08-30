#! /usr/bin/python3
import uuid

from magen_utils_apis.parse_utils import replace_keys
from magen_statistics_api.metric import Metric

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"


class Counter(Metric):
    """
    This class represents Counter statistics type. A counter is a cumulative metric that represents
    a single numerical value that only ever goes up. A counter is typically used to count requests served,
    tasks completed, errors occurred, etc.
    """

    def __init__(self, source, abs_value=0, name=None, period=0, alerts=False, flavor=None):
        """
        Init method

        :param name: any string without spaces; name of Metric
        :param source: string; name of Service that invoked Metric creation
        the update was not received, alert might be invoked (seconds)
        :param abs_value: positive integer; value of the metric upon creation, default = 0
        :param period: positive integer (seconds);
        :param alerts: boolean; trigger property for enabling alerts
        :param flavor: MetricFlavour; with flavour Counter gets certain abilities like auto naming
        """
        if not flavor and not name:
            raise SyntaxError("flavor or name must be provided")
        self.__flavor = flavor
        # if self.__flavor:
        #     name = self.__flavor.title
        super().__init__(name, source, abs_value)
        if not name:
            self.name = source + "." + flavor.flavor_name + "." + flavor.title
        class_name = __class__.__name__
        self.namespace = class_name  # Metric.Counter
        self.__period = period
        self.__alerts = alerts
        self.uuid = str(uuid.uuid4())
        super().metrics_collections.add_to_collection(class_name, self)  # adding new instance to counter collection

    @property
    def flavor(self):
        return self.__flavor

    @flavor.setter
    def flavor(self, value):
        self.__flavor = value

    @property
    def period(self):
        return self.__period

    @period.setter
    def period(self, new_period):
        self.__period = new_period

    @property
    def alerts(self):
        return self.__alerts

    @alerts.setter
    def alerts(self, new_alerts):
        self.__alerts = new_alerts

    def increment(self, value=0):
        """
        Method adds 1 or given value to abs_value property

        :param value: positive integer; value to add to abs_value
        :rtype: void
        """
        if not value:
            self.abs_value += 1
        else:
            self.abs_value += value

    def reset(self):
        """
        Method resets abs_value of counter to 0

        :rtype: void
        """
        self.abs_value = 0

    def to_dict(self):
        data_dict = super().to_dict()
        if not self.provide_detailed_info:
            if not self.flavor:
                return data_dict
            else:
                data_dict["flavor"] = self.flavor.flavor_name
                data_dict["flavor_opt"] = self.flavor.title
                return data_dict
        else:
            pattern = '_' + __class__.__name__ + '__'
            split_str = "__"
            exclude_keys = ["metrics_collections", "provide_detailed_info"]
            data_dict = replace_keys(data_dict, pattern, split_str)
            for key in exclude_keys:
                del data_dict[key]
            if self.flavor:
                data_dict["flavor"] = self.flavor.flavor_name
                data_dict["flavor_opt"] = self.flavor.title
            return data_dict
