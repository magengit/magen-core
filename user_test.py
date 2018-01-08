# coding=utf-8
"""User test for password checks"""

import http
import unittest

import db
from user import main_bp, users_bp, app
from config import DEV_DB_NAME, USER_COLLECTION_NAME
from flask_bcrypt import Bcrypt
from user_model import UserModel


class TestUser(unittest.TestCase):

    def setUp(self):
        # flask_app = Flask(__name__)
        self.bcrypt = Bcrypt(app)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'test_key'
        app.config['SECURITY_PASSWORD_SALT'] = 'test_salt'
        app.register_blueprint(users_bp)
        app.register_blueprint(main_bp)

        self.test_app = app.test_client()
        with db.connect(DEV_DB_NAME) as db_instance:
            db_instance.drop_collection(USER_COLLECTION_NAME)

    def tearDown(self):
        with db.connect(DEV_DB_NAME) as db_instance:
            db_instance.drop_collection(USER_COLLECTION_NAME)

    def test_register_EqualPasswords(self):
        # Register user
        data = {'email': 'test@test.com', 'password': 'testtest1', 'confirm': 'testtest1'}
        self.test_app.post(
            '/register/',
            data=data
        )
        # Same password and confirm password
        self.assertIs(data['password'], data['confirm'])
        with db.connect(DEV_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, data['email'])
            self.assertEqual(result.count, 1)
            user = result.documents
            self.assertTrue(self.bcrypt.check_password_hash(user.password, data['password'].encode()))

    def test_register_NotEqualPasswords(self):
        # Register user
        data2 = {'email': 'test@test.com', 'password': 'testtest1', 'confirm': 'testfail'}
        self.test_app.post(
            '/register/',
            data=data2
        )
        self.assertIsNot(data2['password'],  data2['confirm'])

    def test_login(self):
        # Register user
        data = {'email': 'test@test.com', 'password': 'testtest1', 'confirm': 'testtest1'}
        self.test_app.post(
            '/register/',
            data=data
        )

        # User registered not logged in
        with db.connect(DEV_DB_NAME) as db_instance:
            user_collection = db_instance.get_collection(USER_COLLECTION_NAME)
            result_data = user_collection.find_one({"email": data['email']})
            self.assertEqual(result_data['_is_authenticated'], False)

        # Login user
        post_data = {'email': 'test@test.com', 'password': 'testtest1'}
        resp = self.test_app.post(
            '/login/',
            data=post_data, follow_redirects=True
        )

        # Existing user login with authentication
        with db.connect(DEV_DB_NAME) as db_instance:
            user_collection = db_instance.get_collection(USER_COLLECTION_NAME)
            result_data = user_collection.find_one({"email": post_data['email']})
            self.assertTrue(self.bcrypt.check_password_hash(result_data['password'], post_data['password'].encode()))
            
            self.assertEqual(result_data['_is_authenticated'], True)
            self.assertEqual(resp.status_code, http.HTTPStatus.OK)

        # Non-existing user login
        post_data2 = {'email': 'fail@test.com', 'password': 'testtest1'}
        resp = self.test_app.post(
            '/login/',
            data=post_data2, follow_redirects=True
        )
        with db.connect(DEV_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, post_data2['email'])
            self.assertEqual(result.count, 0)
            self.assertEqual(resp.status_code, http.HTTPStatus.FORBIDDEN)

        # Existing user wrong password login:
        post_data3 = {'email': 'test@test.com', 'password': 'failtest1'}
        resp = self.test_app.post(
            '/login/',
            data=post_data3, follow_redirects=True
        )
        with db.connect(DEV_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, post_data3['email'])
            self.assertEqual(result.count, 1)
            user = result.documents
            self.assertFalse(self.bcrypt.check_password_hash(user.password, post_data3['password'].encode()))
            self.assertEqual(resp.status_code, http.HTTPStatus.FORBIDDEN)
