from functools import wraps

from flask import redirect, session
from urllib.parse import urlencode
import json
from flask import request
import requests
import requests.auth
import logging.config

from magen_id_client_apis.utilities import Utilities
from magen_logger.logger_config import LogDefaults

logger = logging.getLogger(LogDefaults.default_log_name)

__author__ = "michowdh@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class MagenClientAppHandler(object):
    state_key = 'oauthlib.client'

    def __init__(
            self, name,
            issuer="",
            redirect_uris=None,
            callback_uri=None,
            client_id=None,
            client_secret=None,
            response_type=['code', 'id_token', 'id_token token', 'token'],
            default_scopes=None,
            jwt_alg=None,
    ):
        self.name = name
        self.issuer = issuer  # call setter
        self._callback_uri = callback_uri
        self._client_name = name
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uris = redirect_uris
        self._response_type = response_type
        self._default_scopes = default_scopes
        self._jwt_alg = jwt_alg

    @property
    def callback_uri(self):
        """
        This function returns the callback url

        :return: callback_url as string
        :rtype: string
        """
        return self._callback_uri

    @callback_uri.setter
    def callback_uri(self, x):
        """
        This function sets the callback url

        :param x: This parameter contains the callback url
        :type x: string
        """        
        self._callback_uri = x

    @property
    def client_id(self):
        """
        This function returns the client id

        :return: client_id as string
        :rtype: string
        """        
        return self._client_id

    @client_id.setter
    def client_id(self, x):
        """
        This function sets the client id

        :param x: This parameter contains the client id
        :type x: string
        """       
        self._client_id = x

    @property
    def client_secret(self):
        """
        This function returns the client secret

        :return: client_secret as string
        :rtype: string
        """ 
        return self._client_secret

    @client_secret.setter
    def client_secret(self, x):
        """
        This function sets the client secret

        :param x: this parameter contains the client secret
        :type x: string
        """      
        self._client_secret = x

    @property
    def issuer(self):
        """
        This function returns the issuer address

        :return: issuer address as string
        :rtype: string
        """ 
        return self._issuer

    @issuer.setter
    def issuer(self, x):
        """
        This function sets the issuer

        :param x: This parameter contains the issuer
        :type x: string
        """          
        self._issuer = x
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
    def response_type(self, x):
        """
        This function sets the response_type

        :param x: This parameter contains response_type
        :type x: string
        """         
        self._response_type = x

    def authorize(self, username=None, access_token=None, scopes='openid,profile,address', dynamic=False, **kwargs):
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
            logger.debug("_authorize_url===" + self._authorize_url)
            logger.debug("username===" + username)
            logger.debug("self.client_id===" + self._client_id)
            logger.debug("self._callback_uri===" + self._callback_uri)
            logger.debug("scopes===" + scopes)

            state = Utilities.randomstr()
            nonce = Utilities.randomstr()
            session['state'] = state
            session['nonce'] = nonce

            url = Utilities.get_the_encoded_url(
                self._authorize_url + '?username=' + username + '&access_token=' + access_token +
                '&response_type=code' + '&redirect_uri=' + self._callback_uri + '&scope=' + scopes + '&nonce=' + nonce + '&state=' + state)
            url = url + '&client_id=' + self._client_id
            logger.debug("encoded url====" + url)
            return redirect(url)
        except Exception as e:
            logger.error("ERROR: Problem in redirecting.")
            return '/error'

    def process_auth_code(self):
        """

        This function does the following tasks:
            1. checkes the code and state parameter in the returned url
            2. POST submit to the magen_id service with the code, client_id, client_secret, redirect_uri, and grant type
            3. returns the response as json format
        
        :return: json data as an object
        :rtype: json object
        """
        state = request.args.get('state')
        code = request.args.get('code')

        if 'state' is None:
            return {"error": "State is missing"}
        if 'code' is None:
            return {"error": "Authorization code is missing"}

        if "state" in session:
            state_session = session["state"]
            # state_session=state
            if state == state_session:
                code = request.args.get('code')
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
                r = requests.post(
                    self._request_id_token_url, params=access_token_req, headers=headers, verify=False)
                data = json.loads(r.text)

                return data
            else:
                return {"error": "You are not authorizaed. Please try again."}
        else:
            return {"error": "You are not authorizaed. Please try again."}

    def authorized_handler(self, f):
        """

        This is the decorator function for authorized handler
 
        """

        @wraps(f)
        def decorated(*args, **kwargs):
            data = self.process_auth_code()
            return f(*((data,) + args), **kwargs)

        return decorated

    def validate_mid_token_against_id_service(self, id_token, **kwargs):
        """

        This function validates the magen_id_token against the magen_id service and receives
        the detail information of the client and user

        :param id_token: This contains the magen id token 
        :type: string

        return: json data as an object
        rtype: json object 
        """
        logger.debug('======= id_token ========%s ', id_token)
        try:
            headers = {'content-type': 'application/json'}
            response = requests.get(
                self._tokeninfo_url + '?id_token=' + id_token, headers=headers, verify=False)
            me_json = response.json()
        except Exception as e:
            logger.error("ERROR: %s", e)
            return {"error": "token validation is failed"}
        return me_json
