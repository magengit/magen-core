#! /usr/bin/python3
"""Compare Util functions of Core"""

import functools
import json

from magen_utils_apis.parse_utils import flatten_dict_except_keys

__author__ = "alifar_at_cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "09/27/2017"

DEFAULT_IGNORED_KEYS = ['timestamp', 'uuid']


def compare_dicts(expected: dict, actual: dict, transform_f=None):
    """
    Check equality of 2 dictionaries. It can only compare flat dictionaries
    The user can pass transform_f that will do any necessary transformations
    on dictionaries in order to make a comparison

    :param expected: first entry dictionary for comparator
    :type expected: dict
    :param actual: second entry dictionary for comparator
    :type actual: dict
    :param transform_f: function to transform a dictionary for comparison
    :type transform_f: Callable

    :return: compare result
    :rtype: bool
    """
    if transform_f:
        expected_transformed = transform_f(expected)
        actual_transformed = transform_f(actual)
        return expected_transformed == actual_transformed
    return expected == actual


@functools.singledispatch
def default_full_compare(*args):
    """
    Singled Dispatch function that is overloaded by registered type of first argument.
    If unregistered type is passed to this function TypeError is raised.
    Make default full compare for 2 dictionaries, accepts ignored keys.

    First argument may vary as expected value for comparison
    may be stored in different formats
    """
    raise TypeError("type {} is not acceptable".format(type(args[0])))


@default_full_compare.register(dict)
def default_full_compare_dict(expected: dict, actual: dict, excluded_keys=None):
    """
    Default full compare for dict type.

    :param expected: first entry dictionary for comparator
    :type expected: dict
    :param actual: second entry dictionary for comparator
    :type: actual: dict
    :param excluded_keys: keys to be ignored during comparison
    :type excluded_keys: list

    :return: compare result
    :rtype: bool
    """
    ignored_keys = excluded_keys or DEFAULT_IGNORED_KEYS
    partial_flatten_dict = flatten_dict_except_keys(ignored_keys)
    return compare_dicts(expected, actual, partial_flatten_dict)


@default_full_compare.register(str)
def default_full_compare_str(expected: str, actual: dict, excluded_keys=None):
    """
    Default full compare for dict type.

    :param expected: first entry str for comparator (json format)
    :type expected: str
    :param actual: second entry dictionary for comparator
    :type: actual: dict
    :param excluded_keys: keys to be ignored during comparison
    :type excluded_keys: list

    :return: compare result
    :rtype: bool
    """
    expected = json.loads(expected)
    return default_full_compare_dict(expected, actual, excluded_keys)


def full_compare_except_keys(excluded_keys):
    """
    Create a partial function for default_full_compare by passing excluded keys

    :param excluded_keys: keys to be excluded from the dict
    :type excluded_keys: list

    :return: patiral function
    :rtype: Callable
    """
    return functools.partial(default_full_compare, excluded_keys=excluded_keys)


resp_str="""
{
  "response": {
    "asset": {
      "client_uuid": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
      "creation_timestamp": "2016-09-01 21:22:13.053688+00:00",
      "host": "sjc-repenno-nitro10.cisco.com",
      "name": "finance docs",
      "resource_group": "roadmap",
      "resource_id": 3,
      "uuid": "74c1c6ff-c266-43a6-9d14-82dca05cb6df",
      "version": 1
    },
    "cause": 0,
    "success": true
  },
  "status": "201",
  "title": "Asset Creation"
}"""

actual_dict={
  "response": {
    "asset": {
      "name": "finance docs",
      "resource_group": "roadmap",
      "resource_id": 3,
      "uuid": "74c1c6ff-c266-43a6-9d14-82dca05cb6df",
      "version": 1,
      "client_uuid": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
      "creation_timestamp": "2016-09-01 21:22:13.053688+00:00",
      "host": "sjc-repenno-nitro10.cisco.com"
    },
    "cause": 0,
    "success": True
  },
  "status": "201",
  "title": "Asset Creation"
}

if __name__ == "__main__":
    print(default_full_compare(resp_str, actual_dict))
    resp_dict = json.loads(resp_str)
    print(default_full_compare(resp_dict, actual_dict))
    f = full_compare_except_keys(['client_uuid'])
    print(f(resp_str, actual_dict))
