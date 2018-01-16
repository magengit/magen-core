# coding=utf-8
"""
Test Suit for gmail_client.py module
"""

import os
import base64
import unittest
from unittest import mock

from ..magen_gmail_client_api import gmail_client
from ..magen_gmail_client_api import config


class TestGmailClient(unittest.TestCase):

    def setUp(self):
        self.test_creds_dir = os.getcwd() + '/.credentials'
        self.env_mock_data = {
            config.GMAIL_CLIENT_ID: 'non-existing-client_id',
            config.GMAIL_CLIENT_SECRET: 'non-existing-client_secret'
        }

    def tearDown(self):
        if os.path.exists(self.test_creds_dir):
            for filename in os.listdir(self.test_creds_dir):
                os.remove(os.path.join(self.test_creds_dir, filename))
            os.rmdir(self.test_creds_dir)

    def test_get_credentials_json(self):
        """
        Test Generation of Credentials for Gmail API based on Environment
        - gmail_client.get_credentials_env() method
        """
        # Generated data with correct environments
        with mock.patch('os.environ', self.env_mock_data):
            credentials_data = gmail_client.get_credentials_env()
            self.assertIn(self.env_mock_data[config.GMAIL_CLIENT_ID], str(credentials_data))
            self.assertIn(self.env_mock_data[config.GMAIL_CLIENT_SECRET], str(credentials_data))

        # KeyError is generated if environments are not set
        with mock.patch('os.environ', {}):
            self.assertRaises(KeyError, gmail_client.get_credentials_env)

    def test_credentials_user_path(self):
        """ Test Generation of directory and correct path creation - gmail_client.credentials_user_path() method """
        with mock.patch('os.path.expanduser') as home_dir_mock:
            home_dir_mock.return_value = os.getcwd()+'/'  # mocking home_dir to tests dir
            # Verify directory does not exists
            self.assertFalse(os.path.exists(self.test_creds_dir))
            # Creating directory
            created_path = gmail_client.credentials_user_path()
            # Verify directory got created
            self.assertTrue(os.path.exists(self.test_creds_dir))
            # Verify path is correctly constructed
            self.assertIn('json', created_path)
            # Calling function again returns the same result
            self.assertEqual(created_path, gmail_client.credentials_user_path())

    @mock.patch('os.path.expanduser')
    @mock.patch('oauth2client.tools.run_flow')
    @mock.patch('oauth2client.client.OAuth2WebServerFlow')
    @mock.patch('oauth2client.file.Storage')
    def test_gmail_credentials(self, store_mock, oauth_mock, run_flow_mock, os_home_dir_mock):
        """ Test Gmail oAuth Credentials generation - gmail_client.gmail_credentials() method """
        os_home_dir_mock.return_value = os.getcwd() + '/'  # mocking home_dir to tests dir
        # mocking `credentials.invalid` of Gmail API
        store_mock.return_value = mock.Mock()
        store_mock.return_value.get.return_value.invalid = False

        result = gmail_client.gmail_credentials()
        self.assertFalse(result.invalid)  # mock returned unchanged

        store_mock.assert_called_once()

        store_mock.return_value.get.return_value = None
        # Verify correctness of the workflow
        with mock.patch('os.environ', new=self.env_mock_data):
            got_credentials = gmail_client.get_credentials_env()
            gmail_client.gmail_credentials()
        oauth_mock.assert_called_once_with(scope=config.SCOPES, **got_credentials['installed'])
        run_flow_mock.assert_called_once_with(oauth_mock.return_value, store_mock.return_value)

        # KeyError should be thrown
        with mock.patch('os.environ', new={}):
            self.assertIsNone(gmail_client.gmail_credentials())  # on KeyError returns None

    @mock.patch('os.path.expanduser')
    def test_cleanup_cache(self, home_dir_mock):
        """ Test cleanup cache data - gmail_client.cleanup_cache() method """
        test_filenames = ['magen-gmail_test', 'test', 'test.json', 'gmail.test']
        home_dir_mock.return_value = os.getcwd() + '/'  # mocking home_dir to tests dir

        # if folder does not exist - plain return
        gmail_client.cleanup_cache()

        creds_path = os.path.dirname(gmail_client.credentials_user_path())  # creating folder

        # add some tests file to the test directory
        for filename in test_filenames:
            with open(os.path.join(creds_path, filename), '+w') as new_file:
                new_file.write('test')  # write some test data

        gmail_client.cleanup_cache()

        # Assertions
        home_dir_mock.assert_called()
        self.assertTrue(os.path.exists(creds_path))
        self.assertNotIn(config.GMAIL_FILES_PREFIX, os.listdir(creds_path))
        self.assertEqual(len(os.listdir(creds_path)), 3)

    def test_create_message(self):
        """ Test message create - gmail_client.create_messsage() method """
        # Prepare
        test_html_content = '''<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p>
                          <p><a href="some_url">some_url</a></p>
                          <br>
                          <p>Cheers!</p>'''
        test_text_content = 'Please Confirm your email'
        test_sender = 'sender@test.test'
        test_to = 'to@test.test'
        test_subject = 'test'

        # creating email from plain text only
        result_msg = gmail_client.create_message(
            sender=test_sender,
            to=test_to,
            subject=test_subject,
            text_part=test_text_content
        )

        # format required by gmail API
        self.assertIn('raw', result_msg)

        msg_bytes = result_msg['raw'].encode()
        msg_string = base64.urlsafe_b64decode(msg_bytes).decode('utf-8')

        self.assertIn(test_sender, msg_string)
        self.assertIn(test_to, msg_string)
        self.assertIn(test_subject, msg_string)
        self.assertIn(test_text_content, msg_string)

        # creating email from plain text and html content
        result_msg = gmail_client.create_message(
            sender=test_sender,
            to=test_to,
            subject=test_subject,
            text_part=test_text_content,
            html_part=test_html_content
        )

        # format required by gmail API
        self.assertIn('raw', result_msg)

        msg_bytes = result_msg['raw'].encode()
        msg_string = base64.urlsafe_b64decode(msg_bytes).decode('utf-8')

        self.assertIn(test_sender, msg_string)
        self.assertIn(test_to, msg_string)
        self.assertIn(test_subject, msg_string)
        self.assertIn(test_text_content, msg_string)
        self.assertIn(test_html_content, msg_string)

    def test_send_message(self):
        """ Test sending of a message using gmail API """
        test_message = dict(id='test_id')
        gmail_service = mock.Mock()
        gmail_service.users.return_value.messages.return_value.send.return_value.execute.return_value = test_message

        result = gmail_client.send_message(gmail_service, 'here goes email object')
        self.assertIn('id', result)


if __name__ == '__main__':
    unittest.main()
