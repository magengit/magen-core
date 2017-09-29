#! /usr/bin/python3
"""Parsing Util functions of Core"""

import typing
import functools

__author__ = "alifar_at_cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "09/27/2017"


def truncate_keys(dictionary: dict, pattern: str, split_char: str, include_keys=None):
    """
    This function returns a new dictionary with modified truncated keys.

    By provided pattern and split char each key in dict gets split up
    And then new truncate key is added to a new dictionary
    Given dictionary is not modified

    [Note]: include keys expect to get only truncated keys!

    Example::

        test_dict = dict(
            test_key1='test_value1',  # must be truncated
            test_key2='test_value2',  # must be truncated
            key_3='test_value3',
            key4='test_value4'
        )
        truncate_keys(test_dict, 'test', '_')

    Result::
    >>> print(test_dict)
    >>> {'key1': 'test_value1', 'key2': 'test_value2', 'key_3': 'test_value3', 'key4': 'test_value4'}

    :param dictionary: dictionary for iteration
    :type dictionary: dict
    :param pattern: pattern to remove from keys if find_one_filter
    :type pattern: str
    :param split_char: splitting string
    :type split_char: str
    :param include_keys: keys to be included from the result_dict. if empty then all are included
    :type include_keys: list

    :return: new dictionary
    :rtype: dict
    """
    result_dict = dict()
    for prop in dictionary:
        if pattern in prop:
            pattern_list = prop.split(split_char)
            if not include_keys or pattern_list[-1] in include_keys:
                result_dict[pattern_list[-1]] = dictionary[prop]
        else:
            if not include_keys or prop in include_keys:
                result_dict[prop] = dictionary[prop]

    return result_dict


def flatten_dict(data, exclude_keys=None):
    """
    Transforms dictionary into flat list of tuples
    Excluds keys that are specified by the user

    :param data: data to be flatten
    :type data: dict
    :param exclude_keys: keys to be excluded
    :type exclude_keys: list

    :return: flatten data
    :rtype: list
    """
    result = dict()

    def add_to_result(data_dict, key, parent_key):
        """Add to Result list flat items of a dictionary"""
        if exclude_keys and key in exclude_keys:
            return
        cur_key = key if not parent_key else parent_key+(key,)
        result[cur_key] = data_dict[key]

    def visit(data_dict, parent_key=()):
        """
        Recursively visits each dict key in order to collect all items of dict.
        Collects parent key for each item.
        Excludes keys specified by the user

        :param data_dict: data to traverse
        :type: data_dict: dict
        :param parent_key: parent keys for nested dicts
        :type parent_key: tuple

        rtype: void
        """

        for key in data_dict:
            if isinstance(data_dict[key], typing.Dict):
                visit(data_dict[key], parent_key+(key,))
            elif isinstance(data_dict[key], typing.List):
                for item in data_dict[key]:
                    if isinstance(item, typing.Dict):
                        visit(item, parent_key+(key,))
                    else:
                        add_to_result(data_dict, key, parent_key)
                        break
            else:
                add_to_result(data_dict, key, parent_key)

    visit(data_dict=data)
    return result


def flatten_dict_except_keys(exclude_keys):
    """
    Create a partial from flatten_dict() function

    :param exclude_keys: keys that must be excluded from the result
    :type exclude_keys: list

    return partial of flatten_dict
    rtype: Callable
    """
    return functools.partial(flatten_dict, exclude_keys=exclude_keys)


def flatten_dict_result_partial(data, exclude_keys=None):
    """
    Create flat dict from given data and return partial with exclude_keys

    :param data: data to flat
    :type data: dict
    :param exclude_keys: keys to be excluded from the result
    :type exclude_keys: list

    :return: flat result and partial function
    :rtype: tuple
    """
    result = flatten_dict(data, exclude_keys)
    return result, flatten_dict_except_keys(exclude_keys)
