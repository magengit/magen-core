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
        self.dict_with_nested = dict(
            key1='value1',
            key2=['value2', 'value3'],
            key5=dict(
                key6='value4',
                key7=dict(
                    key8='value5'
                )
            )
        )

    def test_one_dict_empty(self):
        """One of the given dicts is empty"""
        self.assertFalse(compare_dicts(self.one_level_dict, {}))
        self.assertFalse(compare_dicts({}, self.one_level_dict))
        self.assertTrue(compare_dicts({}, {}))

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
        # UseCase 4: passing a transformation function to compare_dicts()
        self.assertTrue(compare_dicts(self.one_level_dict, second_dict, _transformation_f))

    def test_complex_dicts(self):
        """Tests with complex dicts (dicts values can be lists or nested dicts)"""
        # UseCase 0: dicts are duplicates
        second_dict = self.dict_with_nested.copy()
        self.assertTrue(compare_dicts(self.dict_with_nested, second_dict))
        # UseCase 1: second dictionary created independently
        second_dict = dict(
            key1='value1',
            key5=dict(
                key7=dict(
                    key8='value5'
                ),
                key6='value4'
            ),
            key2=['value2', 'value3']
        )
        self.assertTrue(compare_dicts(self.dict_with_nested, second_dict))
        # UseCase 2: second dictionary has extra key
        second_dict['test'] = 'test'
        self.assertFalse(compare_dicts(self.dict_with_nested, second_dict))
        # Remove extra key
        second_dict.pop('test')
        self.assertTrue(compare_dicts(self.dict_with_nested, second_dict))
        # UseCase 3: second dictionary has a different value (fisrt level)
        second_dict['key1'] = 'test'
        self.assertFalse(compare_dicts(self.dict_with_nested, second_dict))
        # Roll back correct value
        second_dict['key1'] = self.dict_with_nested['key1']
        self.assertTrue(compare_dicts(self.dict_with_nested, second_dict))
        # UseCase 4: second dictnary has a different value (nested dict value)
        second_dict['key5']['key6'] = 'test'
        self.assertFalse(compare_dicts(self.dict_with_nested, second_dict))
        # Rolla back correct value
        second_dict['key5']['key6'] = self.dict_with_nested['key5']['key6']
        self.assertTrue(compare_dicts(self.dict_with_nested, second_dict))


class TestDefaultFullCompare(unittest.TestCase):
    """Class is a Test Suit for singledispatched function default_full_compare() function"""
    pass
