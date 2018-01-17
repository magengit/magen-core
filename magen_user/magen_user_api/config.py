# coding=utf-8
"""
Config file. Global constants
"""

from flask import Flask
from flask_wtf import CSRFProtect
from flask_login import LoginManager

__copyright__ = "Copyright(c) 2018, Cisco Systems, Inc."
__status__ = "alpha"

TEST_DB_NAME = 'test_magen_demo'
DEV_DB_NAME = 'dev_magen_demo'
PROD_DB_NAME = 'magen_demo'
AUTO_SENDER = 'no-reply@magen.io'

USER_COLLECTION_NAME = 'users'

EXISTING_EMAIL_CODE_ERR = 11000

# creating flask App
app = Flask(__name__)
app.template_folder = 'templates'  # providing path to template folder
app.secret_key = 'test_key'
app.config['WTF_CSRF_ENABLED'] = True
# app.config['WTF_CSRF_SECRET_KEY'] = 'test' # must be secured
app.config['SECRET_KEY'] = 'test_key'  # must be secured
app.config['SECURITY_PASSWORD_SALT'] = 'test_salt'  # must be secured
# configuring application with CSRF protection for form security
CSRFProtect(app)

# configuring application with LoginManger for @login_required and handling login requests
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users_bp.login'

# Initializing hash function and iterations for Pbkdf2 hashing
HASH_FUNCTION = 'sha256'
ITERATIONS = 100000
