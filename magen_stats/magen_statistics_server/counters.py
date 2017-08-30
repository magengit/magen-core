#! /usr/bin/python3

from magen_statistics_api.counter_metric import Counter
from magen_statistics_api.counter_metric_api import get_flavored_counter_instance, CounterAPI

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"

"""
 API for source service to manage counters
"""


def increment(flavor, source, value=0):
    """
    Increment existing counter or Creates a new one and increments it

    :param flavor: Flavor Enum object
    :param source: string
    :param value: integer
    :rtype: void
    """
    counter = get_flavored_counter_instance(flavor)
    if counter:
        counter.increment(value)
    else:
        data = dict()
        data["flavor"] = flavor
        counter = Counter(source, **data)
        counter.increment(value)


def reset(flavor):
    """
    Resets existing counter's absolute value to 0 or does nothing
    reset for flavored counters

    :param flavor: Flavor Enum object
    :rtype: void
    """
    counter = get_flavored_counter_instance(flavor)
    if counter:
        counter.reset()
    # else:
    #     data = dict()
    #     data["flavor"] = flavor
    #     Counter(source, **data)


def delete(flavor):
    """
    Deletes existing flavored counter or does nothing

    :param flavor: Flavored Enum object
    :rtype: void
    """
    CounterAPI.delete_flavored_counter(flavor)
