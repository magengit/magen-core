#! /usr/bin/python3
"""Test Suit for Parsing Util functions"""

import unittest
import typing

from ..magen_utils_apis.parse_utils import truncate_keys, flatten_dict, flatten_dict_except_keys

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
        self.dict_with_nested2 = dict(
            key1='value1',
            key2=dict(
                key3='value2',
                key4='value3'
            ),
            key5=dict(
                key7=dict(
                    key8='value5'
                ),
                key6='value4'
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

    def test_ordered_one_level(self):
        """Simple Dictionary gets flattened"""
        result = flatten_dict(self.one_level_dict, order=True)
        print("\nFlat Dictionary:", result)
        # All keys are transformed into Tuples
        for key in result:
            self.assertIsInstance(key, typing.Tuple)
            # verify values
            self.assertIn('value', result[key])

    def test_ordered_with_nested(self):
        """Flat Dict with nested dicts"""
        result = flatten_dict(self.dict_with_nested, order=True)
        print("\nFlat Dictionary:", result)
        # Flat dictionary length equals number of values
        self.assertEqual(len(result), 5)
        for key in result:
            # verify that every value is value from original dict
            self.assertIn('value', result[key])
            if key == 'key1':  # key1 is on first level
                continue
            # verify that nested dictionary keys are now stored as Tuples
            self.assertIsInstance(key, typing.Tuple)

    def test_ordered_with_list(self):
        """Flat Dict with list of dicts"""
        result = flatten_dict(self.dict_with_lists, order=True)
        print("\nFlat Dictionary:", result)
        # Flat dictionary length equals number of values
        self.assertEqual(len(result), 7)

        for key in result:
            # verify that every value is value from original dict
            self.assertIn('value', result[key])
            # verify that nested dictionary keys are now stored as Tuples
            self.assertIsInstance(key, typing.Tuple)

    def test_flatten_ordered_partial(self):
        """Creation of Partial function"""
        flatten_dict_partial = flatten_dict_except_keys(['key1', 'key2'], order=True)
        result = flatten_dict_partial(self.one_level_dict)
        self.assertEqual(len(result), 2)
        for key in result:
            self.assertIsInstance(key, typing.Tuple)
            self.assertIn('value', result[key])

    def test_one_level_dict(self):
        """Simple Dictionary gets flattened"""
        result = flatten_dict(self.one_level_dict)
        print("\nFlat Dictionary:", result)
        # All keys are transformed into Tuples
        for key in result:
            self.assertIsInstance(key, typing.Tuple)
            # verify all values are sets
            self.assertIsInstance(result[key], typing.Set)

    def test_dict_with_nested(self):
        """Flat Dict with nested dicts. Not ordered nested lists"""
        result = flatten_dict(self.dict_with_nested)
        print("\nFlat Dictionary:", result)
        # Flat dictionary length equals number of values
        self.assertEqual(len(result), 5)
        for key in result:
            # verify that every value is transformed into a set
            self.assertIsInstance(result[key], typing.Set)
            if key == 'key1':  # key1 is on first level
                continue
            # verify that nested dictionary keys are now stored as Tuples
            self.assertIsInstance(key, typing.Tuple)

    def test_dict_with_list(self):
        """Flat Dict with list of dicts. Not ordered nested lists"""
        result = flatten_dict(self.dict_with_lists)
        print("\nFlat Dictionary:", result)

        for key in result:
            # verify that every value is transformed into a set
            self.assertIsInstance(result[key], typing.Set)
            # verify that nested dictionary keys are now stored as Tuples
            self.assertIsInstance(key, typing.Tuple)

        # verify that values are packed as set under single key3
        self.assertEqual(len(result[('key3',)]), 2)
