#! /usr/bin/python3
"""Compare Util functions of Core"""

import functools
import json

from .parse_utils import flatten_dict_except_keys

__author__ = "alifar_at_cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "09/27/2017"

DEFAULT_IGNORED_KEYS = ['creation_timestamp', 'uuid', 'renewal', 'revision', 'expiration']


def _identity(param):
    """Identity returns parameter that passed to it"""
    return param


def compare_dicts(expected: dict, actual: dict, transform_f=_identity):
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
    expected_transformed = transform_f(expected)
    actual_transformed = transform_f(actual)
    return expected_transformed == actual_transformed


@functools.singledispatch
def default_full_compare(*args, **kwargs):
    """
    Singled Dispatch function that is overloaded by registered type of first argument.
    If unregistered type is passed to this function TypeError is raised.
    Make default full compare for 2 dictionaries, accepts ignored keys.

    First argument may vary as expected value for comparison
    may be stored in different formats
    """
    raise TypeError("type {} is not acceptable".format(type(args[0])))


@default_full_compare.register(dict)
def default_full_compare_dict(expected: dict, actual: dict, excluded_keys=None, order=False):
    """
    Default full compare for dict type.

    :param expected: first entry dictionary for comparator
    :type expected: dict
    :param actual: second entry dictionary for comparator
    :type: actual: dict
    :param excluded_keys: keys to be ignored during comparison
    :type excluded_keys: list
    :param order: flag to preserve order in nested lists of dictionaries
    :type order: bool

    :return: compare result
    :rtype: bool
    """
    ignored_keys = list(set().union(excluded_keys, DEFAULT_IGNORED_KEYS)) if excluded_keys else DEFAULT_IGNORED_KEYS
    partial_flatten_dict = flatten_dict_except_keys(ignored_keys, order=order)
    return compare_dicts(expected, actual, partial_flatten_dict)


@default_full_compare.register(str)
def default_full_compare_str(expected: str, actual: dict, excluded_keys=None, order=False):
    """
    Default full compare for dict type.

    :param expected: first entry str for comparator (json format)
    :type expected: str
    :param actual: second entry dictionary for comparator
    :type: actual: dict
    :param excluded_keys: keys to be ignored during comparison
    :type excluded_keys: list
    :param order: flag to preserve order in nested lists of dictionaries
    :type order: bool

    :return: compare result
    :rtype: bool
    """
    expected = json.loads(expected)
    return default_full_compare_dict(expected, actual, excluded_keys, order=order)


def full_compare_except_keys(excluded_keys, order=False):
    """
    Create a partial function for default_full_compare by passing excluded keys

    :param excluded_keys: keys to be excluded from the dict
    :type excluded_keys: list
    :param order: flag to preserve order in nested lists of dictionaries
    :type order: bool

    :return: partial function
    :rtype: Callable
    """
    return functools.partial(default_full_compare, excluded_keys=excluded_keys, order=order)
