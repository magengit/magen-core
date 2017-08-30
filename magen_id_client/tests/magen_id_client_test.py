#! /usr/bin/python3.5
import unittest

from flask import Flask

import magen_core_test_env
from magen_id_client_apis.magen_client import MagenClient
from magen_id_client_apis.utilities import Utilities

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

    def setUp(self):
        self.issuer = self.CONST_ISSUER
        self.client_id = self.CONST_CLIENT_ID
        self.client_secret = self.CONST_CLIENT_SECRET
        self.alg = self.CONST_ALG
        self.request_token_params = self.CONST_REQUEST_TOKEN_PARAM
        self.scopes = self.CONST_SCOPES
        self.username = self.CONST_USERNAME
        self.access_token = self.CONST_ACCESS_TOKEN
        self.state = Utilities.randomstr()
        self.nonce = Utilities.randomstr()
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

    def tearDown(self):
        print("done")

    def test_connected_app(self):
        self.assertEqual(self.connected_app.name, self.CONST_CONNECTED_APP_NAME)
        self.assertEqual(self.connected_app._client_id, self.CONST_CLIENT_ID)
        self.assertEqual(self.connected_app._client_secret, self.CONST_CLIENT_SECRET)
        self.assertEqual(self.connected_app._authorize_url, self.CONST_AUTHORIZE_URL)
        self.assertEqual(self.connected_app._callback_uri, self.CONST_CALLBACK_URL)

        self.connected_app.callback_uri = self.CONST_CALLBACK_URL
        self.assertEqual(self.connected_app.callback_uri, self.CONST_CALLBACK_URL)
        self.connected_app.client_id = self.CONST_CLIENT_ID
        self.assertEqual(self.connected_app.client_id, self.CONST_CLIENT_ID)
        self.connected_app.client_secret = self.CONST_CLIENT_SECRET
        self.assertEqual(self.connected_app.client_secret, self.CONST_CLIENT_SECRET)
        self.connected_app.issuer = self.CONST_ISSUER
        self.assertEqual(self.connected_app.issuer, self.CONST_ISSUER)
        self.connected_app.response_type = self.CONST_RESPONSE_TYPE
        self.assertEqual(self.connected_app.response_type, self.CONST_RESPONSE_TYPE)

    def test_authorize(self):
        expected_url = self.issuer + "/oauth/authorize?username=" + self.username + "&access_token=" + self.access_token + "&response_type=code&redirect_uri=" + self.callback_url + "&scope=" + self.scopes + "&nonce=" + self.nonce + "&state=" + self.state + "&client_id=" + self.client_id
        url = Utilities.get_the_encoded_url(self.connected_app._authorize_url + \
                                            '?username=' + self.username + '&access_token=' + self.access_token + \
                                            '&response_type=code' + '&redirect_uri=' + self.connected_app._callback_uri + \
                                            '&scope=' + self.scopes + '&nonce=' + self.nonce + '&state=' + self.state) + \
                                            '&client_id=' + self.connected_app._client_id

        self.assertEqual(expected_url, url)
        redirect_result = self.connected_app.authorize(username=self.username, access_token=self.access_token)
        redirect_result = self.connected_app.validate_mid_token_against_id_service("erewrewrew434322432")


if __name__ == '__main__':
    unittest.main()
