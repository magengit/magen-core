#! /usr/bin/python3
"""Test Suit for Parsing Util functions"""

import unittest
import typing

from ..magen_utils_apis.parse_utils import truncate_keys, flatten_dict

__author__ = "Alena Lifar"
__email__ = "alifar_at_cisco.com"
__version__ = "0.1"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__status__ = "alpha"


class TestTruncateKeys(unittest.TestCase):
    """Class is a Test Suit for truncate_keys() function"""

    def setUp(self):
        self.test_dict = dict(
            test_key1='test_value1',  # must be truncated
            test_key2='test_value2',  # must be truncated
            key_3='test_value3',
            key4='test_value4'
        )

    def test_empty_dict(self):
        """Empty Dictionary"""
        result = truncate_keys({}, 'test', '_')
        self.assertFalse(result)

    def test_one_key_dict(self):
        """One key in Dict"""
        test_dict = {'test': 'test'}
        result = truncate_keys(test_dict, 'dummy_pattern', 'dummy_split_char')
        self.assertEqual(test_dict, result)

    def test_truncate(self):
        """Truncate Required Keys"""
        test_pattern = 'test'
        test_split_char = '_'
        result = truncate_keys(self.test_dict, test_pattern, test_split_char)
        self.assertEqual(len(result), 4)
        self.assertIn('key1', result)
        self.assertIn('key2', result)

    def test_no_split_char(self):
        """Split Char is not in any key"""
        test_pattern = 'test'
        test_split_char = '.'  # not present in self.test_dict
        result = truncate_keys(self.test_dict, test_pattern, test_split_char)
        self.assertEqual(result, self.test_dict)

    def test_pattern_not_present(self):
        """Pattern is not present in Dictionary"""
        test_pattern = 'tset'  # typo by intention
        test_split_char = '_'
        result = truncate_keys(self.test_dict, test_pattern, test_split_char)
        self.assertEqual(result, self.test_dict)

    def test_include_keys(self):
        """Include specific Keys into the Result"""
        test_pattern = 'test'
        test_split_char = '_'
        # Include keys are truncated
        result = truncate_keys(self.test_dict, test_pattern, test_split_char, include_keys=['key1', 'key2'])
        self.assertEqual(len(result), 2)
        self.assertIn('key1', result)
        self.assertIn('key2', result)


class TestFlattenDict(unittest.TestCase):
    """Class is a Test Suit for flatten_dict() function"""

    def setUp(self):
        self.one_level_dict = dict(
            key1='value1',
            key2='value2',
            key3='value3',
            key4='value4'
        )
        self.dict_with_nested = dict(
            key1='value1',
            key2=dict(
                key3='value2',
                key4='value3'
            ),
            key5=dict(
                key6='value4',
                key7=dict(
                    key8='value5'
                )
            )
        )
        self.dict_with_lists = dict(
            key1='value1',
            key2=[
                dict(
                    key3='value2',
                    key4='value3'
                ),
                dict(
                    key5='value4',
                    key6='value5'
                )
            ],
            key3=['value6', 'value7']  # 6 values in total
        )

    def test_one_level_dict(self):
        """Simple Dictionary gets flattened"""
        result = flatten_dict(self.one_level_dict)
        self.assertEqual(len(result), 4)
        for entry in result:
            # Each entry in result is Tuple
            self.assertIsInstance(entry, typing.Tuple)

    def test_dict_with_nested(self):
        """Flat Dict with nested dicts"""
        result = flatten_dict(self.dict_with_nested)
        self.assertEqual(len(result), 5)  # len always equals to number of values
        for entry in result:
            # Each entry in result is Tuple
            self.assertIsInstance(entry, typing.Tuple)
            # Verify that every second entry in tuples is a value
            self.assertIn('value', entry[1])
        # Verify that parent keys were collceted correctly
        self.assertEqual(result[4][0], ('key5', 'key7', 'key8'))

    def test_dict_with_list(self):
        """Flat Dict with list of dicts"""
        result = flatten_dict(self.dict_with_lists)
        print(result)
        self.assertEqual(len(result), 6)
        # Iterate through all values except the last one which is list
        for index in range(len(result)-1):
            # Each entry in result is Tuple
            self.assertIsInstance(result[index], typing.Tuple)
            # Verify that every second entry in tuples is a value
            self.assertIn('value', result[index][1])
        # Check last entry in result
        self.assertIsInstance(result[len(result)-1][1], typing.List)
        self.assertEqual(len(result[len(result)-1][1]), 2) # key3=['value6', 'value7']
