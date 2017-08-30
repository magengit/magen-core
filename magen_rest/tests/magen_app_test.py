import os
import sys
import unittest

from flask import Flask

import magen_core_test_env

from magen_rest_apis.magen_app import MagenApp

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class MagenAppTest(unittest.TestCase):
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
        magen_app = MagenApp.get_instance().magen
        self.assertIs(magen_app.__class__, Flask)


