#! /usr/bin/python3

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"


def replace_keys(dictionary: dict, pattern: str, split_char: str, include_keys=None):
    """
    This function returns a new dictionary with modified keys

    :param dictionary: dictionary for iteration
    :param pattern: pattern to remove from keys if find_one_filter
    :param split_char: splitting string
    :param include_keys: keys to be included from the result_dict. if empty then all are included

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
