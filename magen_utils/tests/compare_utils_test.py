#! /usr/bin/python3
"""Test Suit for Compare Util functions"""

import unittest
import typing

from ..magen_utils_apis.compare_utils import compare_dicts, default_full_compare, full_compare_except_keys

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
        # UseCase 3: second dictionary has a different value (first level)
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

    def setUp(self):
        self.expected_dict = dict(
            uuid='value1',  # excluded from comparison by default
            key1='value2',
            key2=dict(
                key3='value3',
                key4=True
            ),
            key5=['value5', 'value6']
        )
        # Must be a JSON format
        self.expected_str = """{
            "uuid": "value1",
            "key1": "value2_different",
            "key2": {
                "key3": "value3",
                "key4": true
            },
            "key5": ["value5", "value6"]
        }"""

        self.actual_dict = dict(
            uuid='value1_different',  # excluded from comparison by default
            key1='value2',
            key2=dict(
                key3='value3',
                key4=True
            ),
            key5=['value5', 'value6']
        )

    def test_single_dispatch(self):
        """Test Singledispatch Registry"""
        singledispatch_registry = default_full_compare.registry
        # Verify length of singledispatch registry
        self.assertEqual(len(singledispatch_registry), 3)
        # Verify types registered for default_full_compare()
        self.assertIn(dict, singledispatch_registry.keys())
        self.assertIn(str, singledispatch_registry.keys())

    def test_dict_no_exclude_keys(self):
        """Test Dict type for single discpatch. No excluded keys passed"""
        # Verify dictionary comparison, 'uuid' key is excluded form comparison by default
        self.assertTrue(default_full_compare(self.expected_dict, self.actual_dict))
        # Change actual_dict value:
        self.actual_dict['key1'] = 'value2_different'
        # Verify default_full_compare returns False
        self.assertFalse(default_full_compare(self.expected_dict, self.actual_dict))
        # Roll back correct value
        self.actual_dict['key1'] = self.expected_dict['key1']
        # Equal again
        self.assertTrue(default_full_compare(self.expected_dict, self.actual_dict))

    def test_dict_exclude_keys(self):
        """Test Dict type for single dispatch. Excluded keys test"""
        # Change actual_dict value:
        self.actual_dict['key1'] = 'value2_different'
        # Verify that default excluded keys and passed excluded keys get united
        self.assertTrue(default_full_compare(self.expected_dict, self.actual_dict, ['key1']))
        # Change value of nested dict
        self.actual_dict['key2']['key3'] = 'value3_different'
        # Verify check fails without passing appropriate exclude key
        self.assertFalse(default_full_compare(self.expected_dict, self.actual_dict, ['key1']))
        # Verify check passed if appropriate exclude key passed
        # Note that 'key3' is passed as a raw name without evaluating dict structure (ex. key2.key3)
        # All of keys named 'key3' will be excluded from comparison
        self.assertTrue(default_full_compare(self.expected_dict, self.actual_dict, ['key1', 'key3']))
        # Roll back correct values
        self.actual_dict['key1'] = self.expected_dict['key1']
        self.actual_dict['key2'] = self.expected_dict['key2']
        # Equal again
        self.assertTrue(default_full_compare(self.expected_dict, self.actual_dict))

    def test_string_exclude_keys(self):
        """Test Str type for single discpatch. Excluded keys passed"""
        # Verify dictionary comparison, 'uuid' key is excluded form comparison by default
        # All other features of comparison are available for default_full_compare_str as well
        # And behave the same as tests above
        self.assertTrue(default_full_compare(self.expected_str, self.actual_dict, ['key1']))

    def test_type_error(self):
        """If no dict or str (str must be JSON str) passed Type error raised"""
        with self.assertRaises(TypeError):
            default_full_compare(5, self.actual_dict)
            default_full_compare('444', self.actual_dict)  # passing string should be a JSON format

    def test_partial_full_compare(self):
        """Creation of a Partial Function"""
        self.actual_dict['key1'] = 'value2_different'
        partial_full_compare = full_compare_except_keys(['key1'])
        # Verify that partial function was created
        self.assertIsInstance(partial_full_compare, typing.Callable)
        # Verify that check passes
        self.assertTrue(partial_full_compare(self.expected_dict, self.actual_dict))
