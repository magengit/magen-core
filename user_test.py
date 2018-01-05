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

    def tearDown(self):
        with db.connect(DEV_DB_NAME) as db_instance:
            db_instance.drop_collection(USER_COLLECTION_NAME)

    def test_register(self):
        # Register user
        data = {'email': 'test@test.com', 'password': 'testtest1', 'confirm': 'testtest1'}
        response = self.test_app.post(
            '/register/',
            data=data
        )
        #test Db, bad request, insert into db test
        with db.connect(DEV_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, data['email'])
            self.assertEqual(result.count, 1)
            user = result.documents
            self.assertTrue(self.bcrypt.check_password_hash(user.password, data['password'].encode()))
            # not found not needed here
            self.assertEqual(response.status_code, http.HTTPStatus.FOUND)

    def test_login(self):
        # Register user
        self.test_app.post(
            '/register/',
            data={'email': 'test@test.com', 'password': 'testtest1', 'confirm': 'testtest1'}
        )

        # Login user
        post_data = {'email': 'test@test.com', 'password': 'testtest1'}
        resp = self.test_app.post(
            '/login/',
            data=post_data
        )
        # tet Db to be used
        # insert first and log in nd test
        with db.connect(DEV_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, post_data['email'])
            self.assertEqual(result.count, 1)
            user = result.documents
            self.assertTrue(self.bcrypt.check_password_hash(user.password, post_data['password'].encode()))
            user_collection = db_instance.get_collection(USER_COLLECTION_NAME)
            result_data = user_collection.find({"email": post_data['email']})
            for i in result_data:
                auth = i['_is_authenticated']
            self.assertEqual(auth, True)
            self.assertEqual(resp.status_code, http.HTTPStatus.FOUND)

