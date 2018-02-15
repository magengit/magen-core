# coding=utf-8
"""
Config file. Global constants
"""
import os
from secrets import token_hex

from flask import Flask
# from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_recaptcha import ReCaptcha

__copyright__ = "Copyright(c) 2018, Cisco Systems, Inc."
__status__ = "alpha"

TEST_DB_NAME = 'test_magen_demo'
DEV_DB_NAME = 'dev_magen_demo'
PROD_DB_NAME = 'magen_demo'
AUTO_SENDER = 'no-reply@magen.io'

USER_COLLECTION_NAME = 'users'

EXISTING_EMAIL_CODE_ERR = 11000

RECAPTCHA_SITE_KEY = 'RECAPTCHA_SITE_KEY'
RECAPTCHA_SECRET_KEY = 'RECAPTCHA_SECRET_KEY'

# creating flask App
app = Flask(__name__)
app.template_folder = 'templates'  # providing path to template folder
app.secret_key = token_hex(16)
# app.config['WTF_CSRF_ENABLED'] = False
# app.config['WTF_CSRF_SECRET_KEY'] = 'test' # must be secured
# app.config['SECRET_KEY'] = 'test_key'  # must be secured
app.config['SECURITY_PASSWORD_SALT'] = 'test_salt'  # must be secured
# configuring application with CSRF protection for form security
# CSRFProtect(app)

# configuring application with LoginManger for @login_required and handling login requests
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users_bp.login'


# initiate recaptcha
def init_recaptcha_with_creds(application):
    """
    Get Credentials from Environment and add them to application configuration

    :rtype: void
    """
    try:
        recaptcha_site_key = os.environ[RECAPTCHA_SITE_KEY]
        recaptcha_secret_key = os.environ[RECAPTCHA_SECRET_KEY]
    except KeyError:
        print('[error] Required Environment Variables are not set: {}, {}'.format(
            RECAPTCHA_SITE_KEY, RECAPTCHA_SITE_KEY))
        recaptcha_site_key = None
        recaptcha_secret_key = None
        application.config['RECAPTCHA_ENABLED'] = False
        pass
    application.config[RECAPTCHA_SITE_KEY] = recaptcha_site_key
    application.config[RECAPTCHA_SECRET_KEY] = recaptcha_secret_key

    return ReCaptcha(app=application)

# Initializing hash function and iterations for Pbkdf2 hashing
HASH_FUNCTION = 'sha256'
ITERATIONS = 100000
