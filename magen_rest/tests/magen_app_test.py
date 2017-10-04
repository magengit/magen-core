"""Test Magen Flask App"""

import unittest
from flask import Flask
from magen_rest_apis.magen_app import MagenApp

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class MagenAppTest(unittest.TestCase):
    """Test Magen Flask App"""
    app = None

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        """
        This function prepares the system for running tests
        """
        pass

    def tearDown(self):
        pass

    def test_MagenApp(self):
        """Check that Magen App is a Flask instance"""
        magen_app = MagenApp.get_instance().magen
        self.assertIs(magen_app.__class__, Flask)
