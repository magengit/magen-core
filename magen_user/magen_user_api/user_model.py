# coding=utf-8
"""
User Model. Users Mongo Database Interface
"""

import unittest
import uuid

import pymongo
from magen_mongo_apis.mongo_return import MongoReturn
from magen_utils_apis.datetime_api import SimpleUtc

from magen_user_api.config import TEST_DB_NAME, USER_COLLECTION_NAME
from magen_user_api import db

__copyright__ = "Copyright(c) 2018, Cisco Systems, Inc."
__status__ = "alpha"


def generate_salt():
    """ Returns generated salt value"""
    salt = uuid.uuid4().hex
    return salt


def _cursor_helper(cursor):
    """ Returns processed list """
    result = list()
    for cur in cursor:
        if cur.get("creation_timestamp"):
            cur["creation_timestamp"] = cur["creation_timestamp"].replace(
                tzinfo=SimpleUtc()).isoformat()
        result.append(cur)
    return result


class UserModel(object):
    """
    User Model represents a User Entity
    """
    created_index = False

    def __init__(self, db_ctx, email, password, salt, _is_authenticated=False, **kwargs):
        """
        User Model constructor

        :param db_ctx: Database context
        :type db_ctx: PyMongo.MongoClient.Database
        :param email: Primary Key for user, email
        :type email: str
        :param password: User's secret hash
        :type password: str
        :param salt: Random value
        :type salt: str
        :param is_authenticated: Authentication flag
        :type is_authenticated: bool
        :param kwargs: user's details

        .. notes:: kwargs may contain:
        - first_name
        - second_name
        - role
        - ...
        """
        self.db_ctx = db_ctx
        self.email = email
        self.password = password
        self.salt = salt
        self._is_authenticated = kwargs.pop('_is_authenticated', _is_authenticated)
        self._is_anonymous = kwargs.pop('_is_anonymous', False)
        self._is_active = kwargs.pop('_is_active', True)
        self.confirmed = kwargs.pop('confirmed', False)
        self.confirmed_on = kwargs.pop('confirmed_on', None)
        self.details = kwargs

    def is_active(self):
        """True, as all users are active for now."""
        return self._is_active

    def get_id(self):
        """ Return the email address to satisfy Flask-Login's requirements. """
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self._is_authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return self._is_anonymous

    def _to_dict(self):
        """
        Convert properties to dictionary

        :return: flat dictionary with properties
        :rtype: dict
        """
        attributes = vars(self)
        attributes.pop('db_ctx')
        for detail in attributes['details']:
            attributes[detail] = attributes['details'][detail]
        del attributes['details']
        return attributes

    def submit(self):
        """
        Submit data into Database.
        Uses db.connect Context Manager.
        Implementation is specific to PyMongo package

        :return: Return Object
        :rtype: Object
        """
        user_collection = self.db_ctx.get_collection(USER_COLLECTION_NAME)
        if not type(self).created_index:
            user_collection.create_index('email', unique=True)
        return_obj = MongoReturn()
        try:
            result = user_collection.update_one({'email': self.email}, {"$set": self._to_dict()}, upsert=True)
            if result.acknowledged and result.upserted_id:
                return_obj.success = True
                return_obj.count = 1
                return_obj.message = 'Document inserted successfully'
            elif result.acknowledged and (result.modified_count or result.matched_count):
                return_obj.success = True
                return_obj.matched_count = 1
                return_obj.count = 1
                return_obj.message = 'Document updated successfully'
            else:
                return_obj.success = False
                return_obj.count = 0
                return_obj.message = "Failed to insert document"
            return return_obj
        except pymongo.errors.PyMongoError as error:
            return_obj.success = False
            return_obj.code = error.code
            return_obj.message = error.details
            return_obj.db_exception = error
            return return_obj

    @classmethod
    def select_by_email(cls, db_instance, email):
        """
        Select a User by email

        :param db_instance:

        :param email: user's e-mail
        :type email: str

        :return: found users or empty list
        :rtype: MongoReturn
        """
        user_collection = db_instance.get_collection(USER_COLLECTION_NAME)

        seed = dict(email=email)
        projection = dict(_id=False)

        mongo_return = MongoReturn()
        try:
            cursor = user_collection.find(seed, projection)
            result = _cursor_helper(cursor)
            assert len(result) == 1 or len(result) == 0
            mongo_return.success = True
            if len(result):
                mongo_return.documents = cls(db_instance, **result[0])  # email is unique index
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
        with db.connect(TEST_DB_NAME) as db_instance:
            db_instance.drop_collection(USER_COLLECTION_NAME)

    def tearDown(self):
        with db.connect(TEST_DB_NAME) as db_instance:
            db_instance.drop_collection(USER_COLLECTION_NAME)

    def test_upsert(self):
        """
        Insert User into Mongo DB Test
        """
        test_email = 'test@test.com'
        test_password = 'test_password'
        test_salt = generate_salt()
        user_details = dict(
            first_name='Joe',
            last_name='Dow'
        )

        # Insert new document
        with db.connect(TEST_DB_NAME) as db_instance:
            user_obj = UserModel(db_instance, test_email, test_password, test_salt, **user_details)
            result_obj = user_obj.submit()

        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.count, 1)

        # Insert same document
        with db.connect(TEST_DB_NAME) as db_instance:
            user_obj = UserModel(db_instance, test_email, test_password, test_salt, **user_details)
            result_obj = user_obj.submit()

        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.matched_count, 1)
        self.assertEqual(result_obj.count, 1)

        # Update existing document
        test_password = 'testing_password'
        user_details = dict(
            first_name='John',
            last_name='Doe'
        )
        with db.connect(TEST_DB_NAME) as db_instance:
            user_obj = UserModel(db_instance, test_email, test_password, test_salt, **user_details)
            result_obj = user_obj.submit()
        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.matched_count, 1)
        # comparing values with DB
        user_collection = db_instance.get_collection(USER_COLLECTION_NAME)
        user = user_collection.find_one({"email": test_email})

        self.assertEqual(user['password'], test_password)
        self.assertEqual(user['first_name'], user_details['first_name'])
        self.assertEqual(user['last_name'], user_details['last_name'])

    def test_select_by_email(self):
        """
        Select user by email (unique value)
        """
        test_email = 'test@test.com'
        test_password = 'test_password'
        test_salt = generate_salt()
        user_details = dict(
            first_name='Joe',
            last_name='Dow'
        )

        # Select non-existing document
        with db.connect(TEST_DB_NAME) as db_instance:
            result_obj = UserModel.select_by_email(db_instance, test_email)
        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.count, 0)

        # Insert new document
        with db.connect(TEST_DB_NAME) as db_instance:
            user_obj = UserModel(db_instance, test_email, test_password, test_salt, **user_details)
            result_obj = user_obj.submit()

        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.count, 1)

        # Select existing document
        with db.connect(TEST_DB_NAME) as db_instance:
            result_obj = UserModel.select_by_email(db_instance, test_email)
        self.assertTrue(result_obj.success)
        self.assertEqual(result_obj.count, 1)
        user_obj = result_obj.documents
        self.assertEqual(user_obj.email, test_email)
