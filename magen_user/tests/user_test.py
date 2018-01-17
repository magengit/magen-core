# coding=utf-8
"""User test for password checks"""

import http
import unittest
from unittest import mock

from ..magen_user_api import config
from ..magen_user_api import db, user_api
from ..magen_user_api.user_model import UserModel


class TestUser(unittest.TestCase):

    def setUp(self):
        config.app.config['TESTING'] = True
        config.app.config['WTF_CSRF_ENABLED'] = False
        config.app.config['SECRET_KEY'] = 'test_key'
        config.app.config['SECURITY_PASSWORD_SALT'] = 'test_salt'
        config.app.config['SERVER_NAME'] = 'app'
        config.app.register_blueprint(user_api.users_bp)
        config.app.register_blueprint(user_api.main_bp)

        self.test_app = config.app.test_client()
        with db.connect(config.TEST_DB_NAME) as db_instance:
            db_instance.drop_collection(config.USER_COLLECTION_NAME)
        config.DEV_DB_NAME = config.TEST_DB_NAME

    def tearDown(self):
        with db.connect(config.TEST_DB_NAME) as db_instance:
            db_instance.drop_collection(config.USER_COLLECTION_NAME)

    def test_register_EqualPasswords(self):
        data = {'email': 'test@test.com', 'password': 'testtest1', 'confirm': 'testtest1'}
        # Register user
        with mock.patch('magen_user.magen_user_api.user_api.send_confirmation'):
            self.test_app.post(
                '/register/',
                data=data
            )
        # Same password and confirm password
        self.assertIs(data['password'], data['confirm'])

        # Checking password hashing
        with db.connect(config.DEV_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, data['email'])
            self.assertEqual(result.count, 1)
            user = result.documents
            self.assertTrue(user_api.check_password_hash(user.password, user.salt, data['password'].encode('utf-8')))

    def test_register_NotEqualPasswords(self):
        # Register user
        data2 = {'email': 'test@test.com', 'password': 'testtest1', 'confirm': 'testfail'}
        with mock.patch('magen_user.magen_user_api.user_api.send_confirmation'):
            self.test_app.post(
                '/register/',
                data=data2
            )
        self.assertIsNot(data2['password'],  data2['confirm'])

    def test_login(self):
        # Register user
        data = {'email': 'test@test.com', 'password': 'testtest1', 'confirm': 'testtest1'}
        with mock.patch('magen_user.magen_user_api.user_api.send_confirmation'):
            self.test_app.post(
                '/register/',
                data=data
            )

        # User registered not logged in
        with db.connect(config.TEST_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, data['email'])
            user = result.documents
            self.assertEqual(user._is_authenticated, False)

        # Login user
        post_data = {'email': 'test@test.com', 'password': 'testtest1'}
        resp = self.test_app.post(
            '/login/',
            data=post_data, follow_redirects=True
        )

        # Existing user login with authentication
        with db.connect(config.TEST_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, post_data['email'])
            user = result.documents
            self.assertTrue(user_api.check_password_hash(user.password, user.salt,
                                                         post_data['password'].encode()))

            self.assertEqual(user._is_authenticated, True)
            self.assertEqual(resp.status_code, http.HTTPStatus.OK)

        # Non-existing user login
        post_data2 = {'email': 'fail@test.com', 'password': 'testtest1'}
        resp = self.test_app.post(
            '/login/',
            data=post_data2, follow_redirects=True
        )
        with db.connect(config.TEST_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, post_data2['email'])
            self.assertEqual(result.count, 0)
            self.assertEqual(resp.status_code, http.HTTPStatus.FORBIDDEN)

        # Existing user wrong password login:
        post_data3 = {'email': 'test@test.com', 'password': 'failtest1'}
        resp = self.test_app.post(
            '/login/',
            data=post_data3, follow_redirects=True
        )
        with db.connect(config.TEST_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, post_data3['email'])
            self.assertEqual(result.count, 1)
            user = result.documents
            self.assertFalse(
                user_api.check_password_hash(user.password, user.salt, post_data3['password'].encode('utf-8')))
            self.assertEqual(resp.status_code, http.HTTPStatus.FORBIDDEN)

    def test_generate_confirm_token(self):
        """ Test token generation from user email """
        test_user_email = 'test@test.test'
        generated_token = user_api.generate_confirmation_token(test_user_email)
        email = user_api.confirm_token(generated_token)
        self.assertEqual(email, test_user_email)

        # token expired
        email = user_api.confirm_token(generated_token, -2)
        self.assertFalse(email)
        generated_token = 'test_generated_token.rrr'
        # token is invalid
        email = user_api.confirm_token(generated_token)
        self.assertFalse(email)
        # signature and token bad format
        generated_token = 'test_generated_token'
        email = user_api.confirm_token(generated_token)
        self.assertFalse(email)

    @mock.patch('magen_gmail_client_api.gmail_client.connect')
    @mock.patch('magen_gmail_client_api.gmail_client.send_message')
    @mock.patch('flask.render_template')
    def test_send_confirmation(self, template_mock, send_msg_mock, gmail_connect_mock):
        """ Test confirmation of an email on User Registration """
        template_mock.return_value = '<p>Welcome!test html msg</p>'
        gmail_connect_mock.return_value.__enter__.return_value.name = 'gmail_service'
        test_user_email = 'test@test.test'
        with mock.patch('flask.url_for') as confirm_url_mock:
            confirm_url_mock.return_value = 'test_url'
            with config.app.app_context():
                user_api.send_confirmation(test_user_email)
        template_mock.assert_called_once_with('email_confirmation.html', confirm_url='test_url', user_email=test_user_email)

    def test_confirm_email(self):
        """ Test confirmation of a user's email. /confirm/<token> route """
        test_user_email = 'test@test.test'
        test_password = 'testtest1'

        # Register user
        data = {'email': test_user_email, 'password': test_password, 'confirm': test_password}
        with mock.patch('magen_user.magen_user_api.user_api.send_confirmation'):
            self.test_app.post(
                '/register/',
                data=data
            )

        # invalid token provided
        resp = self.test_app.get('/confirm/'+'invalid_token', follow_redirects=True)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)

        # redirected to login page
        self.assertIn('password', resp.data.decode('utf-8'))
        self.assertIn('email', resp.data.decode('utf-8'))

        with db.connect(config.TEST_DB_NAME) as db_instance:
            user = UserModel.select_by_email(db_instance, test_user_email).documents
        self.assertFalse(user.confirmed)
        self.assertFalse(user._is_authenticated)

        correct_token = user_api.generate_confirmation_token(email=test_user_email)
        resp = self.test_app.get('/confirm/' + correct_token, follow_redirects=True)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)

        # redirected to login page
        self.assertIn('password', resp.data.decode('utf-8'))
        self.assertIn('email', resp.data.decode('utf-8'))

        with db.connect(config.TEST_DB_NAME) as db_instance:
            user = UserModel.select_by_email(db_instance, test_user_email).documents
        self.assertTrue(user.confirmed)
        self.assertTrue(user._is_authenticated)
