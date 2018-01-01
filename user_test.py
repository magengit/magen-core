# coding=utf-8
"""User test for password checks"""

import http
import unittest

import db
from user import main_bp, users_bp, app
from config import DEV_DB_NAME, USER_COLLECTION_NAME


class TestUser(unittest.TestCase):

    def setUp(self):
        # flask_app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'test_key'
        app.config['SECURITY_PASSWORD_SALT'] = 'test_salt'
        app.register_blueprint(users_bp)
        app.register_blueprint(main_bp)

        self.test_app = app.test_client()

    def tearDown(self):
        with db.connect(DEV_DB_NAME) as db_instance:
            db_instance.drop_collection(USER_COLLECTION_NAME)

    def test_login(self):
        # Register user
        self.test_app.post(
            '/register/',
            data={'email': 'test@test.com', 'password': 'testtest1', 'confirm': 'testtest1'}
        )

        # Login user
        resp = self.test_app.post(
            '/login/',
            data={'email': 'test@test.com', 'password': 'testtest1'}
        )
        self.assertEqual(resp.status_code, http.HTTPStatus.FOUND)

