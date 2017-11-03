"""Magen Client Handler handles authorization requests to Magen ID service"""
from functools import wraps
from urllib.parse import urlencode
import logging
import json
import flask
import requests
import requests.auth
import functools
from http import HTTPStatus

from magen_id_client_apis import utilities
from magen_rest_apis.rest_exception_apis import handle_specific_exception
from magen_rest_apis.rest_return_api import RestReturn
from magen_logger.logger_config import LogDefaults

LOGGER = logging.getLogger(LogDefaults.default_log_name)

__author__ = "michowdh@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class MagenClientAppHandler(object):
    """Magen Client Application Handler. Performs authorization requests to Magen ID Service"""
    DEFAULT_RESPONSE_TYPES = ['code', 'id_token', 'id_token token', 'token']
    state_key = 'oauthlib.client'

    def __init__(
            self, name,
            issuer="",
            redirect_uris=None,
            callback_uri=None,
            client_id=None,
            client_secret=None,
            response_type=None,
            default_scopes=None,
            jwt_alg=None,
    ):
        self.name = name
        self._issuer = issuer  # call setter
        self._callback_uri = callback_uri
        self._client_name = name
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uris = redirect_uris
        self._response_type = response_type or MagenClientAppHandler.DEFAULT_RESPONSE_TYPES
        self._default_scopes = default_scopes
        self._jwt_alg = jwt_alg
        self._authorize_url = self._issuer + '/oauth/authorize'
        self._request_id_token_url = self._issuer + '/oauth/token'
        self._tokeninfo_url = self._issuer + '/oauth/tokeninfo'

    @property
    def callback_uri(self):
        """
        This function returns the callback url

        :return: callback_url as string
        :rtype: string
        """
        return self._callback_uri

    @callback_uri.setter
    def callback_uri(self, url_string):
        """
        This function sets the callback url

        :param url_string: This parameter contains the callback url
        :type url_string: string
        """
        self._callback_uri = url_string

    @property
    def client_id(self):
        """
        This function returns the client id

        :return: client_id as string
        :rtype: string
        """
        return self._client_id

    @client_id.setter
    def client_id(self, new_id):
        """
        This function sets the client id

        :param new_id: This parameter contains the client id
        :type new_id: string
        """
        self._client_id = new_id

    @property
    def client_secret(self):
        """
        This function returns the client secret

        :return: client_secret as string
        :rtype: string
        """
        return self._client_secret

    @client_secret.setter
    def client_secret(self, new_secret):
        """
        This function sets the client secret

        :param new_secret: this parameter contains the client secret
        :type new_secret: string
        """
        self._client_secret = new_secret

    @property
    def issuer(self):
        """
        This function returns the issuer address

        :return: issuer address as string
        :rtype: string
        """
        return self._issuer

    @issuer.setter
    def issuer(self, new_issuer):
        """
        This function sets the issuer

        :param new_issuer: This parameter contains the issuer
        :type new_issuer: string
        """
        self._issuer = new_issuer
        self._authorize_url = self._issuer + '/oauth/authorize'
        self._request_id_token_url = self._issuer + '/oauth/token'
        self._tokeninfo_url = self._issuer + '/oauth/tokeninfo'

    @property
    def response_type(self):
        """
        This function returns the response_type

        :return: response_type as string
        :rtype: string
        """
        return self._response_type

    @response_type.setter
    def response_type(self, new_response_type):
        """
        This function sets the response_type

        :param new_response_type: This parameter contains response_type
        :type new_response_type: string
        """
        self._response_type = new_response_type

    def authorize(self, username=None, access_token=None, scopes='openid,profile,address', dynamic=False):
        """
        This function takes five parameters and redirects the client request to the magen_id service.

        :param username: This parameter contains the username of the user
        :param access_token: This parameter contains the Access token that comes from the user IDP
        :param scopes: This parameter contains the scope like email, profile, address, etc.
        :param dynamic: This parameter contains the flag for dynamic or non-dynamic client registration
        :type username: string
        :type access_token: string
        :type scopes: string
        :type dynamic: boolean
        """
        try:
            LOGGER.debug("_authorize_url===" + self._authorize_url)
            LOGGER.debug("username===" + username)
            LOGGER.debug("self.client_id===" + self._client_id)
            LOGGER.debug("self._callback_uri===" + self._callback_uri)
            LOGGER.debug("scopes===" + scopes)
            LOGGER.debug("dynamic mode=== " + str(dynamic))

            state = utilities.randomstr()
            nonce = utilities.randomstr()
            flask.session['state'] = state
            flask.session['nonce'] = nonce

            url = utilities.get_the_encoded_url(
                self._authorize_url + '?username=' + username + '&access_token=' + access_token +
                '&response_type=code' + '&redirect_uri=' + self._callback_uri + '&scope=' + scopes +
                '&nonce=' + flask.session['nonce'] + '&state=' + flask.session['state'])
            url = url + '&client_id=' + self._client_id
            LOGGER.debug("encoded url====" + url)
            # result = send_request(flask.redirect, url=url)
            # try:
            return flask.redirect(url)
            # except requests.exceptions.RequestException as err:
            #     return handle_specific_exception(err)
            # return RestReturn(
            #     success=True,
            #     message="Authorization Request",
            #     http_status=HTTPStatus.OK,
            #     json_body=response,
            #     response_object=response
            # )
        except Exception as error:
            LOGGER.error("ERROR: invalid url encoding: %s", error)
            # return RestReturn(
            #     success=False,
            #     message="Invalid URL encoding",
            #     json_body={"error": "Invalid url encoding"}
            # )
            return '/error'

    def process_auth_code(self):
        """

        This function does the following tasks:
            1. checkes the code and state parameter in the returned url
            2. POST submit to the magen_id service with the code, client_id,
               client_secret, redirect_uri, and grant type
            3. returns the response as json format

        :return: json data as an object
        :rtype: json object
        """
        state = flask.request.args.get('state', None)
        code = flask.request.args.get('code', None)

        if state is None:
            return {"error": "State is missing"}
        if code is None:
            return {"error": "Authorization code is missing"}

        if state == flask.session.get("state", None):
            access_token_req = {
                "code": code,
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "redirect_uri": self._callback_uri,
                "grant_type": "authorization_code",
            }
            headers = {}
            content_length = len(urlencode(access_token_req))
            access_token_req['content-length'] = str(content_length)
            try:
                response = requests.post(
                    url=self._request_id_token_url,
                    params=access_token_req,
                    headers=headers,
                    verify=False
                )
            except requests.exceptions.RequestException as err:
                return handle_specific_exception(err)
            return RestReturn(
                success=True,
                message="Process Authorization Code",
                http_status=HTTPStatus.OK,
                json_body=json.loads(response.text),
                response_object=response
            )
        return RestReturn(
            success=False,
            message="Authorization Failed",
            http_status=HTTPStatus.UNAUTHORIZED,
            json_body={"error": "You are not authorizaed. Please try again."}
        )

    def authorized_handler(self, func):
        """
        This is the decorator function for authorized handler
        """

        @wraps(func)
        def decorated(*args, **kwargs):
            data = self.process_auth_code()
            return func(*((data,) + args), **kwargs)

        return decorated

    def validate_mid_token_against_id_service(self, id_token):
        """
        This function validates the magen_id_token against the magen_id service and receives
        the detail information of the client and user

        :param id_token: This contains the magen id token
        :type: string

        return: json data as an object
        rtype: json object
        """
        LOGGER.debug('======= id_token ========%s ', id_token)
        headers = {'content-type': 'application/json'}
        partial_return = functools.partial(RestReturn, message='Validate MID token')
        try:
            response = requests.get(
                url=self._tokeninfo_url + '?id_token=' + id_token,
                headers=headers,
                verify=False
            )
        except requests.exceptions.RequestException as err:
            return handle_specific_exception(err)
        return partial_return(
            success=True,
            http_status=HTTPStatus.OK,
            json_body=response.json(),
            response_object=response
        ) if response.status_code == HTTPStatus.OK else partial_return(
            success=False,
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            json_body={"error": "token validation is failed"},
            response_object=None
        )
