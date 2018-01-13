# coding=utf-8
"""
Global Configurations for core packages
"""
import os

GMAIL_CLIENT_ID = 'GMAIL_CLIENT_ID'
GMAIL_CLIENT_SECRET = 'GMAIL_CLIENT_SECRET'
GMAIL_SECRETS_FILE = 'gmail_secrets.json'
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
APPLICATION_NAME = 'Gmail API Python for Magen'
SECRETS_USER_FOLDER = '.credentials'
GMAIL_FILES_PREFIX = 'magen-gmail'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
