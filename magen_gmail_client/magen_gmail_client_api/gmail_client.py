# coding=utf-8
"""
Gmail Client for Magen. Obtain Gmail credentials, connection and send messages
"""
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from contextlib import contextmanager

import httplib2
import os
import json

from apiclient import discovery
from googleapiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client import file

from magen_gmail_client.magen_gmail_client_api import config

PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))


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
    credential_dir = os.path.join(home_dir, config.SECRETS_USER_FOLDER)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, config.GMAIL_FILES_PREFIX+'-python.json')
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
    api_credentials = store.get()
    if not api_credentials or api_credentials.invalid:
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
        api_credentials = tools.run_flow(oauth_flow, store)
    return api_credentials


def cleanup_cache():
    """
    Clean Up Gmail API cache data from the user space
    :return: None
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, config.SECRETS_USER_FOLDER)
    if not os.path.exists(credential_dir):
        return
    # gmail cached files to be deleted
    filenames = [_ for _ in os.listdir(credential_dir) if config.GMAIL_FILES_PREFIX in _]
    for filename in filenames:
        os.remove(os.path.join(credential_dir, filename))
    try:
        os.rmdir(credential_dir)
    except OSError:
        print('{} is not empty'.format(credential_dir))
        pass


def create_message(sender, to, subject, text_part, html_part=None):
    """Create a message for an email.

    :param sender: Email address of the sender.
    :param to: Email address of the receiver.
    :param subject: The subject of the email message.
    :param text_part: The text of the email message.
    :param html_part: The html content of the email message if any.

    :return: An object containing a base64url encoded email object.

    Note: for emails embedded html both test_part and html_part is frequently required by mailing clients.
    """
    if html_part:
        message = MIMEMultipart('alternative')
        msg_txt_part = MIMEText(text_part)
        msg_html_part = MIMEText(html_part, 'html')
        message.attach(msg_txt_part)
        message.attach(msg_html_part)
    else:
        message = MIMEText(text_part)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_msg = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_msg.decode('utf-8')}


def send_message(service, message, user_id='me'):
    """Send an email message.

    :param service: Authorized Gmail API service instance.
    :param message: Message to be sent.
    :param user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.

    :return: Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error: # pragma: no cover
        print('An error occurred: %s' % error)


@contextmanager
def connect(cleanup=False):
    """
    Context Manager for Gmail API connection
    :param cleanup: flag to require credentials cleanup after the operation
    :type cleanup: bool
    :return: generator with Gmail Service object
    """
    try:
        credentials = gmail_credentials()
        http = credentials.authorize(httplib2.Http())
        gmail_service = discovery.build('gmail', 'v1', http=http)
        yield gmail_service
    finally:
        # TODO: some additional cleanup (?)
        if cleanup:
            cleanup_cache()
