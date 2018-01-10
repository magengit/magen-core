# coding=utf-8
"""
Test Suit for gmail_client.py module
"""

import unittest
import mock

import config
from ..gmail_client_api.gmail_client import get_credentials_env


class TestGmailClient(unittest.TestCase):

    def test_get_credentials_json(self):
        """
        Test Generation of Credentials for Gmail API based on Environment
        """
        mock_data = {
            config.GMAIL_CLIENT_ID: 'non-existing-client_id',
            config.GMAIL_CLIENT_SECRET: 'non-existing-client_secret'
        }
        # Generated data with correct environments
        with mock.patch('os.environ', mock_data):
            credentials_data = get_credentials_env()
            self.assertIn(mock_data[config.GMAIL_CLIENT_ID], str(credentials_data))
            self.assertIn(mock_data[config.GMAIL_CLIENT_SECRET], str(credentials_data))

        # KeyError is generated if environments are not set
        with mock.patch('os.environ', {}):
            self.assertRaises(KeyError, get_credentials_env)


if __name__ == '__main__':
    unittest.main()
