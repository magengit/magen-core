# coding=utf-8
"""
Global Configurations for core packages
"""
import os

GMAIL_CLIENT_ID = 'GMAIL_CLIENT_ID'
GMAIL_CLIENT_SECRET = 'GMAIL_CLIENT_SECRET'
GMAIL_SECRETS_FILE = 'gmail_secrets.json'
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
APPLICATION_NAME = 'Gmail API Python for Magen'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
