#! /usr/bin/python3
"""Test Suit for Compare Util functions"""

import unittest

from magen_utils_apis.compare_utils import compare_dicts

__author__ = "Alena Lifar"
__email__ = "alifar_at_cisco.com"
__version__ = "0.1"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__status__ = "alpha"

def _transformation_f(data: dict):
    """Example transformation function for compare_dicts()"""
    data['test_key'] = 'test'
    return data


class TestCompareDicts(unittest.TestCase):
    """Class is a Test Suit for compare_dicts() function"""

    def setUp(self):
        self.one_level_dict = dict(
            key1='value1',
            key2='value2',
            key3='value3',
            key4='value4'
        )

    def test_one_dict_empty(self):
        """One of the given dicts is empty"""
        self.assertFalse(compare_dicts(self.one_level_dict, {}))

    def test_one_level_dicts(self):
        """Tests with flat dicts"""
        # UseCase 0: dicts are duplicates
        second_dict = self.one_level_dict.copy()
        self.assertTrue(compare_dicts(self.one_level_dict, second_dict))
        # UseCase 1: second dictionary created independently
        second_dict = dict(
            key3='value3',
            key1='value1',
            key2='value2',
            key4='value4'
        )
        self.assertTrue(compare_dicts(self.one_level_dict, second_dict))
        # UseCase 2: second dictionary has extra key
        second_dict['key5'] = 'value5'
        self.assertFalse(compare_dicts(self.one_level_dict, second_dict))
        # Remove extra key
        second_dict.pop('key5')
        self.assertTrue(compare_dicts(self.one_level_dict, second_dict))
        # UseCase 3: second dictionary has different value(-s)
        second_dict['key1'] = 'test'
        second_dict['key4'] = 'test'
        self.assertFalse(compare_dicts(self.one_level_dict, second_dict))
        # Roll back correct values
        second_dict['key1'] = self.one_level_dict['key1']
        second_dict['key4'] = self.one_level_dict['key4']
        self.assertTrue(compare_dicts(self.one_level_dict, second_dict))
