#! /usr/bin/python3
import json
import sys
import uuid
import unittest
from unittest.mock import Mock, patch

import pymongo
import os
from pymongo.errors import BulkWriteError
from pymongo.results import InsertOneResult, InsertManyResult, DeleteResult

import magen_core_test_env
from magen_mongo_apis.mongo_core_database import MongoCore
from .magen_test_db import MagenTestDb
from .magen_test_db_strategy import MagenTestDbStrategy

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"

MONGO_PORT = 27017


BULK_WRITE_ERROR_JSON_STR = """
{
  "nInserted": 0,
  "nMatched": 1,
  "nModified": 1,
  "nRemoved": 0,
  "nUpserted": 0,
  "upserted": [],
  "writeConcernErrors": [],
  "writeErrors": [
    {
      "code": 11000,
      "errmsg": "...E11000...duplicate key error...",
      "index": 1,
      "op": {
        "_id": 4
      }
    }
  ]
}"""


class MagenMongoApisTest(unittest.TestCase):
    magen_test_db = None
    magen_test_db_strategy = None
    LOCAL_MONGO_LOCATOR = None

    @classmethod
    def setUpClass(cls):
        try:
            mongo_ip_port = os.environ["MONGO_IP_PORT"]
            mongo_ip = mongo_ip_port.split(":")[0]
            cls.LOCAL_MONGO_LOCATOR = "{ip}:{port}".format(ip=mongo_ip, port=MONGO_PORT)
        except KeyError:
            cls.LOCAL_MONGO_LOCATOR = "{ip}:{port}".format(ip='127.0.0.1', port=MONGO_PORT)
            print("Using local Mongo")
        print(cls.LOCAL_MONGO_LOCATOR)
        cls.magen_test_db = MagenTestDb.get_instance()
        cls.magen_test_db.magen_test_collection.drop()
        cls.magen_test_db_strategy = MagenTestDbStrategy.get_instance()
        db_list = cls.magen_test_db.mongo_client.database_names()
        # 'analytics_db', 'key_db', 'local', 'magen', 'magen_service_registry', 'magen_test'
        for db_name in db_list:
            if db_name != "local":
                cls.magen_test_db.mongo_client.drop_database(db_name)

    def setUp(self):
        self.magen_test_db.magen_test_collection.drop()

    def tearDown(self):
        pass

    def test_Bulk_InvalidOperation(self):

        bulk_obj = self.magen_test_db_strategy.initialize_bulk_operation()
        db_return = self.magen_test_db_strategy.execute_bulk_operation(bulk_obj)
        self.assertIs(db_return.db_exception.__class__, pymongo.errors.InvalidOperation)

    def test_Bulk(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"
        test_document_dict["location"] = "San Jose"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = str(uuid.uuid4())
        test_document_dict2["name"] = "InsertOne"
        test_document_dict2["location"] = "Tokyo"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"
        test_document_dict3["location"] = "Paris"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 2)

        bulk_obj = self.magen_test_db_strategy.initialize_bulk_operation()

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"
        test_document_dict3["locations"] = ["Paris"]

        self.magen_test_db_strategy.bulk_insert(bulk_obj, test_document_dict3)
        self.magen_test_db_strategy.bulk_remove_one(bulk_obj, test_document_dict["uuid"])
        self.magen_test_db_strategy.bulk_remove_one(bulk_obj, test_document_dict2["uuid"])

        doc_filter = {"uuid":  test_document_dict3["uuid"]}
        action = {"locations": "Beijing"}
        #
        self.magen_test_db_strategy.bulk_add_to_set(bulk_obj, doc_filter, action)
        db_return = self.magen_test_db_strategy.execute_bulk_operation(bulk_obj)
        self.assertEqual(db_return.success, True)
        db_return = self.magen_test_db_strategy.find_one_filter({"locations": ["Paris", "Beijing"]})
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)

        db_return = self.magen_test_db_strategy.count_documents({})
        self.assertEqual(db_return.count, 1)

    def test_AddToSet(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"
        test_document_dict["locations"] = ["San Jose", "Tokyo", "Paris"]

        db_return = self.magen_test_db_strategy.insert(test_document_dict)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)

        doc_filter = {"uuid": test_document_dict["uuid"]}
        action = {"locations": "Beijing"}

        db_return = self.magen_test_db_strategy.add_to_set(doc_filter, action)
        self.assertEqual(db_return, True)

    def test_AddToSet_DocNotFound(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"
        test_document_dict["locations"] = ["San Jose", "Tokyo", "Paris"]

        db_return = self.magen_test_db_strategy.insert(test_document_dict)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)

        doc_filter = {"uuid": str(uuid.uuid4())}
        action = {"locations": "Beijing"}

        db_return = self.magen_test_db_strategy.add_to_set(doc_filter, action)
        self.assertEqual(db_return, False)

    def test_Replace_ReplaceNotAcknowledged(self):

        test_document_dict4 = dict()
        test_document_dict4["uuid"] = str(uuid.uuid4())
        test_document_dict4["location"] = "Beijing"

        doc_filter = {"uuid": str(uuid.uuid4())}
        mock = Mock(return_value=None)
        with patch('pymongo.collection.Collection.find_one_and_replace', new=mock):
            db_return = self.magen_test_db_strategy.replace(doc_filter, test_document_dict4)
            self.assertEqual(db_return.documents, [])
            self.assertEqual(db_return.success, False)

    def test_Replace(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"
        test_document_dict["location"] = "San Jose"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = str(uuid.uuid4())
        test_document_dict2["name"] = "InsertOne"
        test_document_dict2["location"] = "Tokyo"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"
        test_document_dict3["location"] = "Paris"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

        test_document_dict4 = dict()
        test_document_dict4["uuid"] = str(uuid.uuid4())
        test_document_dict4["location"] = "Beijing"

        doc_filter = {"uuid": test_document_dict["uuid"]}

        db_return = self.magen_test_db_strategy.replace(doc_filter, test_document_dict4)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.documents["uuid"], test_document_dict4["uuid"])

    def test_DeleteAll_DeleteNotAcknowledged(self):
        mock = Mock(return_value=DeleteResult(acknowledged=False, raw_result=None))
        with patch('pymongo.collection.Collection.delete_many', new=mock):
            db_return = self.magen_test_db_strategy.delete_all()
            self.assertEqual(db_return.success, False)
            self.assertEqual(db_return.count, 0)

    def test_DeleteAll(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = str(uuid.uuid4())
        test_document_dict2["name"] = "InsertOne"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

        db_return = self.magen_test_db_strategy.delete_all()
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

    def test_DeleteNonExistentDoc(self):

        doc_filter = {"uuid": str(uuid.uuid4())}

        db_return = self.magen_test_db_strategy.delete(doc_filter)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 0)

    def test_Delete_DeleteNotAcknowledged(self):

        doc_filter = {"uuid": str(uuid.uuid4())}

        mock = Mock(return_value=DeleteResult(acknowledged=False, raw_result=None))
        with patch('pymongo.collection.Collection.delete_one', new=mock):
            db_return = self.magen_test_db_strategy.delete(doc_filter)
            self.assertEqual(db_return.success, False)
            self.assertEqual(db_return.count, 0)

    def test_Delete(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = str(uuid.uuid4())
        test_document_dict2["name"] = "InsertOne"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

        doc_filter = {"uuid": test_document_dict["uuid"]}

        db_return = self.magen_test_db_strategy.delete(doc_filter)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)

        db_return = self.magen_test_db_strategy.select_all()
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 2)

    def test_FindOneFilter_DocNotFound(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = str(uuid.uuid4())
        test_document_dict2["name"] = "InsertOne"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

        doc_filter = {"uuid": str(uuid.uuid4())}
        db_return = self.magen_test_db_strategy.find_one_filter(doc_filter)
        self.assertEqual(db_return.success, False)
        self.assertEqual(db_return.count, 0)

    def test_FindOneFilter(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = str(uuid.uuid4())
        test_document_dict2["name"] = "InsertOne"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

        doc_filter = {"uuid": test_document_dict["uuid"]}
        db_return = self.magen_test_db_strategy.find_one_filter(doc_filter)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)

    def test_SelectByCondition(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = str(uuid.uuid4())
        test_document_dict2["name"] = "InsertOne"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

        doc_filter = {"uuid": test_document_dict["uuid"]}
        db_return = self.magen_test_db_strategy.select_by_condition(doc_filter)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)

    def test_SelectAll(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = test_document_dict["uuid"]
        test_document_dict2["name"] = "InsertOne"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = test_document_dict["uuid"]
        test_document_dict3["name"] = "InsertOne"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)
        db_return = self.magen_test_db_strategy.select_all()
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

    def test_InsertMany_InsertNotAcknowledged(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = test_document_dict["uuid"]
        test_document_dict2["name"] = "InsertOne"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = test_document_dict["uuid"]
        test_document_dict3["name"] = "InsertOne"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        mock = Mock(return_value=InsertManyResult(acknowledged=True, inserted_ids=[]))
        with patch('pymongo.collection.Collection.insert_many', new=mock):
            db_return = self.magen_test_db_strategy.insert_many(test_document_dict)
            self.assertEqual(db_return.success, False)
            self.assertEqual(db_return.count, 0)

    def test_UpdateMany(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = test_document_dict["uuid"]
        test_document_dict2["name"] = "InsertOne"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = test_document_dict["uuid"]
        test_document_dict3["name"] = "InsertOne"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)
        doc_filter = {"uuid": test_document_dict["uuid"]}
        action = {'$set': {'name': sys._getframe().f_code.co_name}}
        db_return = self.magen_test_db_strategy.update_many(doc_filter, action)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

    def test_UpdateMany_UpdateNotAcknowledged(self):

        doc_filter = {"uuid": str(uuid.uuid4())}
        action = {'$set': {'name': sys._getframe().f_code.co_name}}
        db_return = self.magen_test_db_strategy.update_many(doc_filter, action)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 0)

    def test_UpdateOne(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"
        db_return = self.magen_test_db_strategy.insert(test_document_dict)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)
        doc_filter = {"uuid": test_document_dict["uuid"]}
        action = {'$set': {'name': sys._getframe().f_code.co_name}}
        db_return = self.magen_test_db_strategy.update(doc_filter, action)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)

    def test_UpdateOne_UpdateNotAcknowledged(self):
        doc_filter = {"uuid": str(uuid.uuid4())}
        action = {'$set': {'name': sys._getframe().f_code.co_name}}
        db_return = self.magen_test_db_strategy.update(doc_filter, action)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 0)

    def test_InsertOne(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = sys._getframe().f_code.co_name
        db_return = self.magen_test_db_strategy.insert(test_document_dict)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)

    def test_InsertOne_InsertNotAcknowledged(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = sys._getframe().f_code.co_name
        mock = Mock(return_value=InsertOneResult(acknowledged=False, inserted_id=None))
        with patch('pymongo.collection.Collection.insert_one', new=mock):
            db_return = self.magen_test_db_strategy.insert(test_document_dict)
            self.assertEqual(db_return.success, False)

    def test_InsertOne_ThrowsOperationFailure(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = sys._getframe().f_code.co_name
        mock = Mock(side_effect=pymongo.errors.OperationFailure("Error", details="Operation Failure"))
        with patch('pymongo.collection.Collection.insert_one', new=mock):
            db_return = self.magen_test_db_strategy.insert(test_document_dict)
            self.assertIs(db_return.db_exception.__class__, pymongo.errors.OperationFailure)

    def test_InsertOne_ThrowsNetworkTimeout(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = sys._getframe().f_code.co_name
        mock = Mock(side_effect=pymongo.errors.NetworkTimeout(message="NetworkTimeout"))
        with patch('pymongo.collection.Collection.insert_one', new=mock):
            db_return = self.magen_test_db_strategy.insert(test_document_dict)
            self.assertIs(db_return.db_exception.__class__, pymongo.errors.NetworkTimeout)

    def test_InsertOne_ThrowsExecutionTimeout(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = sys._getframe().f_code.co_name
        mock = Mock(side_effect=pymongo.errors.ExecutionTimeout("Error", details="ExecutionTimeout"))
        with patch('pymongo.collection.Collection.insert_one', new=mock):
            db_return = self.magen_test_db_strategy.insert(test_document_dict)
            self.assertIs(db_return.db_exception.__class__, pymongo.errors.ExecutionTimeout)

    def test_InsertOne_ThrowsCursorNotFound(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = sys._getframe().f_code.co_name
        mock = Mock(side_effect=pymongo.errors.CursorNotFound("Error", details="CursorNotFound"))
        with patch('pymongo.collection.Collection.insert_one', new=mock):
            db_return = self.magen_test_db_strategy.insert(test_document_dict)
            self.assertIs(db_return.db_exception.__class__, pymongo.errors.CursorNotFound)

    def test_InsertOne_ThrowsPyMongoError(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = sys._getframe().f_code.co_name
        mock = Mock(side_effect=pymongo.errors.PyMongoError())
        with patch('pymongo.collection.Collection.insert_one', new=mock):
            db_return = self.magen_test_db_strategy.insert(test_document_dict)
            self.assertIs(db_return.db_exception.__class__, pymongo.errors.PyMongoError)

    def test_InsertOne_ThrowsBulkWriteError(self):
        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = sys._getframe().f_code.co_name
        mock = Mock(side_effect=pymongo.errors.BulkWriteError(results=json.loads(BULK_WRITE_ERROR_JSON_STR)))
        with patch('pymongo.collection.Collection.insert_one', new=mock):
            db_return = self.magen_test_db_strategy.insert(test_document_dict)
            self.assertIs(db_return.db_exception.__class__, pymongo.errors.BulkWriteError)

    def test_CountDocuments(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"
        test_document_dict["location"] = "San Jose"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = str(uuid.uuid4())
        test_document_dict2["name"] = "InsertOne"
        test_document_dict2["location"] = "Tokyo"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"
        test_document_dict3["location"] = "Paris"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

        doc_filter = {"uuid": test_document_dict["uuid"]}

        db_return = self.magen_test_db_strategy.count_documents(doc_filter)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 1)

    def test_CountDocuments_DocNotFound(self):

        test_document_dict = dict()
        test_document_dict["uuid"] = str(uuid.uuid4())
        test_document_dict["name"] = "InsertOne"
        test_document_dict["location"] = "San Jose"

        test_document_dict2 = dict()
        test_document_dict2["uuid"] = str(uuid.uuid4())
        test_document_dict2["name"] = "InsertOne"
        test_document_dict2["location"] = "Tokyo"

        test_document_dict3 = dict()
        test_document_dict3["uuid"] = str(uuid.uuid4())
        test_document_dict3["name"] = "InsertOne"
        test_document_dict3["location"] = "Paris"

        test_document_list = list()
        test_document_list.append(test_document_dict)
        test_document_list.append(test_document_dict2)
        test_document_list.append(test_document_dict3)

        db_return = self.magen_test_db_strategy.insert_many(test_document_list)
        self.assertEqual(db_return.success, True)
        self.assertEqual(db_return.count, 3)

        doc_filter = {"uuid": str(uuid.uuid4())}

        db_return = self.magen_test_db_strategy.count_documents(doc_filter)
        self.assertEqual(db_return.success, False)
        self.assertEqual(db_return.count, 0)

    def test_MongoCore(self):
        core_database = MongoCore.get_instance()
        core_database.client_strategy = MagenTestDb.get_instance()
        core_database.user_strategy = MagenTestDb.get_instance()
        core_database.group_strategy = MagenTestDb.get_instance()
        core_database.utils_strategy = MagenTestDb.get_instance
        core_database.resource_strategy = MagenTestDb.get_instance()
        core_database.policy_template_strategy = MagenTestDb.get_instance()
        core_database.policy_instance_strategy = MagenTestDb.get_instance()
        core_database.policy_contract_strategy = MagenTestDb.get_instance()
        core_database.policy_session_strategy = MagenTestDb.get_instance()
        core_database.settings_strategy = MagenTestDb.get_instance()
        core_database.mis_session_strategy = MagenTestDb.get_instance()
        # global LOCAL_MONGO_LOCATOR
        # print("LOCAL %s" % MagenMongoApisTest.LOCAL_MONGO_LOCATOR)
        core_database.db_ip_port = MagenMongoApisTest.LOCAL_MONGO_LOCATOR
        core_database.initialize()

        db_list = core_database.get_mongo_client().database_names()
        print(db_list)
