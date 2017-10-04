#! /usr/bin/python3.5
"""Magen ID Client Test Suite"""
import unittest
import flask
from flask import Flask
from unittest.mock import Mock, patch, MagicMock
from http import HTTPStatus

from ..magen_id_client_apis.magen_client import MagenClient
from ..magen_id_client_apis import utilities

__author__ = "Mizanul Chowdhury"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "michowdh@cisco.com"


class MagenIdClientTestCase(unittest.TestCase):
    CONST_ISSUER = 'https://ids.clus16-magen.com'
    CONST_CLIENT_ID = 'VqFfbs2YBfuwPkepwYIrdhwkjnlICX4kdlT2Lnd4MAOfnJMtTRreS4nEn6Xc'
    CONST_CLIENT_SECRET = 'yd0C3p2tNZKXH5HsvJVP0v8atQgIoM'
    CONST_ALG = 'HS256'
    CONST_REQUEST_TOKEN_PARAM = {'scope': 'email,profile'}
    CONST_SCOPES = 'openid,profile,address'
    CONST_USERNAME = 'michowdh@cisco.com'
    CONST_ACCESS_TOKEN = 'some_token'
    CONST_CALLBACK_URL = "https://localhost:5228/oauth/callback"
    CONST_CONNECTED_APP_NAME = 'box_magen_agent'
    CONST_AUTHORIZE_URL = 'https://ids.clus16-magen.com/oauth/authorize'
    CONST_RESPONSE_TYPE = "code"
    CONST_ID_TOKEN = 'erewrewrew434322432'

    def setUp(self):
        self.issuer = self.CONST_ISSUER
        self.client_id = self.CONST_CLIENT_ID
        self.client_secret = self.CONST_CLIENT_SECRET
        self.alg = self.CONST_ALG
        self.request_token_params = self.CONST_REQUEST_TOKEN_PARAM
        self.scopes = self.CONST_SCOPES
        self.username = self.CONST_USERNAME
        self.access_token = self.CONST_ACCESS_TOKEN
        self.state = utilities.randomstr()
        self.nonce = utilities.randomstr()
        self.callback_url = self.CONST_CALLBACK_URL

        app = Flask(__name__)
        magen_client = MagenClient(app)
        self.connected_app = magen_client.register_client_app(
            'box_magen_agent',
            issuer=self.issuer,
            client_id=self.client_id,
            client_secret=self.client_secret,
            callback_uri=self.callback_url,
        )
        self.connected_app.response_type = self.CONST_RESPONSE_TYPE

    def tearDown(self):
        print("done")

    def test_connected_app(self):
        self.assertEqual(self.connected_app.name, self.CONST_CONNECTED_APP_NAME)
        self.assertEqual(self.connected_app.client_id, self.CONST_CLIENT_ID)
        self.assertEqual(self.connected_app.client_secret, self.CONST_CLIENT_SECRET)
        self.assertEqual(self.connected_app.callback_uri, self.CONST_CALLBACK_URL)
        self.assertEqual(self.connected_app.issuer, self.CONST_ISSUER)
        self.assertEqual(self.connected_app.response_type, self.CONST_RESPONSE_TYPE)

    @patch.object(flask, 'redirect')
    @patch('requests.get')
    def test_authorize(self, requests_mock, redirect_mock):
        """This methods tests main methods of Magen Client Handler"""
        redirect_mock.return_value = Mock()
        redirect_mock.return_value.json.return_value = 'Mocked Response'
        requests_mock.return_value = Mock()
        requests_mock.return_value.json.return_value = 'Mocked Response'

        expected_url = "{0}/oauth/authorize?username={1}&access_token=" \
                       "{2}&response_type=code&redirect_uri={3}&scope={4}&nonce={5}&state={6}&client_id={7}".\
            format(self.issuer, self.username, self.access_token, self.callback_url,
                   self.scopes, self.nonce, self.state, self.client_id)

        # Mocking and replacing a Flask session object
        session_mock = MagicMock()
        session_dict = {'state': self.state, 'nonce': self.nonce}
        session_mock.__getitem__.side_effect = session_dict.__getitem__
        with patch('flask.session', new=session_mock):
            # executing authorize method with patched session mock object
            redirect_response = self.connected_app.authorize(username=self.username, access_token=self.access_token)

        # Verifying the whole scenario was executed correctly
        self.assertTrue(redirect_response.success)
        self.assertEqual(redirect_response.http_status, HTTPStatus.OK)
        self.assertEqual(redirect_response.json_body, requests_mock.return_value.json.return_value)
        # Assertion of expected url passed to flask.redirect()
        redirect_mock.assert_called_once_with(expected_url)

        # Executing validate_mid_token method
        validation_response = self.connected_app.validate_mid_token_against_id_service(
            MagenIdClientTestCase.CONST_ID_TOKEN
        )
        # Verifying the whole scenario was executed correctly
        self.assertTrue(validation_response.success)
        self.assertEqual(validation_response.http_status, HTTPStatus.OK)
        self.assertEqual(validation_response.json_body, requests_mock.return_value.json.return_value)
        # Assertion of expected url passed to requests.get()
        expected_token_url = self.issuer + '/oauth/tokeninfo' + '?id_token=' + MagenIdClientTestCase.CONST_ID_TOKEN
        expected_headers = {'content-type': 'application/json'}
        expected_verify = False
        requests_mock.assert_called_once_with(
            headers=expected_headers,
            url=expected_token_url,
            verify=expected_verify
        )


if __name__ == '__main__':
    unittest.main()
