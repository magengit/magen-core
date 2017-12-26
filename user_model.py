# coding=utf-8
"""
User Model. Users Mongo Database Interface
"""

import pymongo
from pymongo import MongoClient
import unittest

from config import DEV_DB_NAME, TEST_DB_NAME
from magen_utils_apis.datetime_api import SimpleUtc
from magen_mongo_apis.mongo_return import MongoReturn


def _cursor_helper(cursor):
    """Returns processed list"""
    result = list()
    for cur in cursor:
        if cur.get("creation_timestamp"):
            cur["creation_timestamp"] = cur["creation_timestamp"].replace(
                tzinfo=SimpleUtc()).isoformat()
        result.append(cur)
    return result


class UsersDb(object):
    """Users Database Interface"""

    def __init__(self, db_name=DEV_DB_NAME):
        """
        Users DB Interface Init
        :param db_name: name of database
        :type db_name: str
        """
        mongo_client = MongoClient()
        users_db = mongo_client.get_database(db_name)
        self.users_collection = users_db.get_collection('users')
        self.users_collection.create_index('email', unique=True)

    def insert(self, user_data: dict):
        """
        Insert User into DB

        :param user_data: user data to be inserted
        :type user_data: dict

        :return: Return Object
        :rtype: Object
        """
        return_obj = MongoReturn()
        try:
            result = self.users_collection.insert_one(user_data.copy())
            if result.acknowledged and result.inserted_id:
                return_obj.success = True
                return_obj.count = 1
                return_obj.message = 'Document inserted successfully'
            else:
                return_obj.success = False
                return_obj.message = "Failed to insert document"
            return return_obj
        except pymongo.errors.PyMongoError as error:
            return_obj.success = False
            return_obj.code = error.code
            return_obj.message = error.details
            return_obj.db_exception = error
            return return_obj

    def select_user_by_email(self, email: str):
        """
        Select a User by email

        :param email: user's e-mail
        :type email: str

        :return: found users or empty list
        :rtype: list
        """
        seed = dict(email=email)
        projection = dict(_id=False)

        mongo_return = MongoReturn()
        try:
            cursor = self.users_collection.find(seed, projection)
            result = _cursor_helper(cursor)
            mongo_return.success = True
            mongo_return.documents = result
            mongo_return.count = len(result)
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            mongo_return.success = False
            mongo_return.documents = error.details
            mongo_return.code = error.code
            return mongo_return


class TestUserDB(unittest.TestCase):
    """
    Test for Users DB
    """

    def setUp(self):
        self.test_users = UsersDb(TEST_DB_NAME)

    def tearDown(self):
        mongo_client = MongoClient()
        mongo_client.drop_database(TEST_DB_NAME)

    def test_insert(self):
        """
        Insert User into Mongo DB Test
        """
        user_data = dict(
            email='test@test.com',
            password='test_password',
            confirm_password='test_password',
            first_name='Joe',
            last_name='Dow'
        )

        # Insert new document
        result_obj = self.test_users.insert(user_data)
        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.count, 1)

        # Insert same document
        result_obj = self.test_users.insert(user_data)
        self.assertFalse(result_obj.success)
        self.assertEqual(result_obj.count, 0)
        self.assertEqual(result_obj.code, 11000)  # duplicate exception code

    def test_select_by_email(self):
        """
        Select user by email (unique value)
        """
        test_email = 'test@test.com'
        user_data = dict(
            email=test_email,
            password='test_password',
            confirm_password='test_password',
            first_name='Joe',
            last_name='Dow'
        )

        # Select non-existing document
        result_obj = self.test_users.select_user_by_email(test_email)
        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.count, 0)

        # Insert new document
        result_obj = self.test_users.insert(user_data)
        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.count, 1)

        # Select existing document
        result_obj = self.test_users.select_user_by_email(test_email)
        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.count, 1)
        entry = result_obj.documents[0]
        self.assertEqual(entry['email'], test_email)
