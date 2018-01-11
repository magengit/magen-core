# coding=utf-8
"""

"""

import httplib2
import os
import sys
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client import file

import config

PACKAGE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_credentials_env():
    """
    Get Credentials from Environment and return credential data

    :return: Credential Data
    :rtype: JSON
    """
    try:
        gmail_client_id = os.environ[config.GMAIL_CLIENT_ID]
        gmail_client_secret = os.environ[config.GMAIL_CLIENT_SECRET]
    except KeyError:
        print('[error] Required Environment Variables are not set: {}, {}'.format(
            config.GMAIL_CLIENT_ID, config.GMAIL_CLIENT_SECRET))
        raise
    with open(PACKAGE_PATH+'/credentials/'+config.GMAIL_SECRETS_FILE) as f:
        data = f.read()

    data = json.loads(data)
    data['installed']['client_id'] = gmail_client_id
    data['installed']['client_secret'] = gmail_client_secret
    return data


def credentials_user_path():
    """
    After oAuth flow is run once, credentials file is created and stored in user home_dir
    This allows to refer to this hidden file after logged in for the first time.

    :return: path to credentials file
    :rtype: str
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python.json')
    return credential_path


def gmail_credentials():
    """
    oAuth flow for Gmail API client.
    If credentials don't exist generates them out of Environment
    Stores updated or generated credentials in user home_dir.

    :return: credentials
    :rtype: object
    """
    store = file.Storage(credentials_user_path())
    credentials = store.get()
    if not credentials or credentials.invalid:
        try:
            cred_data = get_credentials_env()
        except KeyError as err:
            print(err)
            return None
        cred_data_parsed = cred_data['installed']
        oauth_flow = client.OAuth2WebServerFlow(
            scope=config.SCOPES,
            **cred_data_parsed
        )
        print(cred_data_parsed)
        print(oauth_flow)
        oauth_flow.user_agent = config.APPLICATION_NAME
        credentials = tools.run_flow(oauth_flow, store)
    return credentials


if __name__ == '__main__':
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(os.environ)
    print(get_credentials_env())
    print(gmail_credentials())
