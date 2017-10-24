"""Concrete Base Abstract Class implemenation of Dao Interface from magen-datastore"""
import logging
from abc import ABCMeta, abstractmethod

import pymongo
from pymongo import ReturnDocument
from magen_utils_apis.datetime_api import SimpleUtc
from magen_logger.logger_config import LogDefaults
from magen_datastore_apis.dao_interface import IDao

from .mongo_exception_apis import handle_specific_exception
from .mongo_return import MongoReturn
from .mongo_utils import MongoUtils

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


def _cursor_helper(cursor):
    """Returns processed list"""
    result = list()
    for cur in cursor:
        if cur.get("creation_timestamp"):
            cur["creation_timestamp"] = cur["creation_timestamp"].replace(
                tzinfo=SimpleUtc()).isoformat()
        result.append(cur)
    return result


class Dao(IDao, metaclass=ABCMeta):
    """
    Concrete implementation of IDao class
    Is a base class for concrete Collection classes
    Some methods might be overridden or new methods can be implemented
    This is just basic DAO for all the collections
    Abstract methods must be implemented in collection class
    """

    __instance = None
    uuid_field_name = "uuid"

    def __init__(self, magen_logger):
        self.logger = magen_logger

    @classmethod
    def get_instance(cls, magen_logger=None):
        """Get Singleton Instance"""
        if cls.__instance is None:
            cls.__instance = cls(magen_logger or logging.getLogger(LogDefaults.default_log_name))
        return cls.__instance

    @abstractmethod
    def get_collection(self):
        """Get Collection from the database"""
        pass

    def initialize_bulk_operation(self):
        """
        Initialize a Mongo Bulk Ordered Operation

        :rtype: Bulk Obj
        """
        bulk = self.get_collection().initialize_ordered_bulk_op()
        return bulk

    def execute_bulk_operation(self, bulk_obj):
        """
        Execute a series of db operations packed in a single bulk transaction

        :param bulk_obj: Bulk Operation Object
        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            bulk_result = bulk_obj.execute()
            return MongoUtils.check_bulk_operation_result(bulk_result)
        except pymongo.errors.InvalidOperation as error:
            # This is not really an error but just an indication
            # that the bulk operation was empty.
            mongo_return.success = True
            mongo_return.db_exception = error
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def bulk_insert(self, bulk_obj, data):
        """
        Add insert operation to bulk operation

        :param bulk_obj: Bulk Operation Object
        :param data: The data dict to be inserted
        :rtype: void
        """
        bulk_obj.insert(data)

    def bulk_remove_one(self, bulk_obj, uuid):
        """
        Add delete operation to bulk operation

        :param bulk_obj: Bulk Operation Object
        :param uuid: UUid of document to be removed
        :rtype: void
        """
        bulk_obj.find({self.uuid_field_name: uuid}).remove_one()

    def bulk_add_to_set(self, bulk_obj, dict_seed, action_dict):
        """
        Adds a element to an array of an existing document

        :param bulk_obj: Bulk Operation Object
        :param dict_seed: Filter of document to be matched
        :param action_dict: Array and element to be added
        :rtype: void
        """
        new_bulk_obj = bulk_obj.find(dict_seed).update_one(
            {"$addToSet": action_dict})
        return new_bulk_obj

    def add_to_set(self, dict_seed, action_dict):
        # FIXME this function needs to be MongoREturn
        """
        Adds a element to an array of an existing document

        :param dict_seed: Filter of document to be matched
        :param action_dict: Array and element to be added
        :rtype: boolean
        """
        try:
            update_result = self.get_collection().update_one(dict_seed, {"$addToSet": action_dict})
            if update_result.acknowledged and update_result.modified_count:
                return True
            return False
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def update(self, dict_seed, action_dict):
        """
        Update document with new data. Fields will be modified or created

        :param dict_seed: Dict representing a filter query
        :param action_dict: Dict representing element to be updated
        [Note] action_dict must contain a Mongo Update Operator that represents an action for update:

        Name	        Description
        $currentDate	Sets the value of a field to current date, either as a Date or a Timestamp.
        $inc	        Increments the value of the field by the specified amount.
        $min	        Only updates the field if the specified value is less than the existing field value.
        $max	        Only updates the field if the specified value is greater than the existing field value.
        $mul	        Multiplies the value of the field by the specified amount.
        $rename	        Renames a field.
        $set	        Sets the value of a field in a document.
        $setOnInsert	Sets the value of a field if an update results in an insert of a document.
                        Has no effect on update operations that modify existing documents.
        $unset	        Removes the specified field from a document.

        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            update_result = self.get_collection().update_one(dict_seed, action_dict)
            mongo_return.success = update_result.acknowledged
            mongo_return.count = update_result.modified_count
            mongo_return.matched_count = update_result.matched_count
            if update_result.acknowledged and update_result.modified_count:
                mongo_return.message = "Update successful"
            else:
                mongo_return.message = "Update failed"
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def update_many(self, dict_seed, action_dict):
        """
        Update many documents with new data. Fields will be modified or created

        :param dict_seed: Dict representing a filter query
        :param action_dict: Dict representing element to be updated
        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            update_result = self.get_collection().update_many(dict_seed, action_dict)
            mongo_return.success = update_result.acknowledged
            mongo_return.count = update_result.modified_count
            mongo_return.matched_count = update_result.matched_count
            if update_result.acknowledged and update_result.modified_count:
                mongo_return.message = "Update successful"
            else:
                mongo_return.message = "Update failed"
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def select_by_condition(self, seed, projection=None):
        """
        Select documents based on filter

        :param projection: Mongo projection
        :param seed: Dict representing a filter query
        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            if not projection:
                projection = dict()
            projection['_id'] = False
            cursor = self.get_collection().find(seed, projection)
            result = _cursor_helper(cursor)
            mongo_return.success = True
            mongo_return.documents = result
            mongo_return.count = len(result)
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def insert(self, data, additional_data=None):
        """
        This function inserts a record in the DB if it does not already
        exists. This is the bottom most function therefore any consistency
        checks and sanitization happened way before we got here.

        :param data: Document to be inserted in the dictionary
        :param additional_data: dictionary of dependency record
        that must be added as a reference (ex: mongo_user.py)
        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            result = self.get_collection().insert_one(data.copy())
            if result.acknowledged and result.inserted_id:
                mongo_return.success = True
                mongo_return.message = "Document inserted successfully"
                mongo_return.count = 1
            else:
                mongo_return.success = False
                mongo_return.message = "Failed to insert document"
                self.logger.error("Failed to insert document")
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def insert_many(self, data_list):
        """
        Insert many documents within a single API call

        :param data_list: List of dicts. A list of documents to be inserted.
        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            result = self.get_collection().insert_many(data_list.copy())
            mongo_return.count = len(result.inserted_ids)
            if result.acknowledged and (len(result.inserted_ids) == len(data_list)):
                mongo_return.success = True
                mongo_return.message = "Documents inserted"
                # return True
            else:
                mongo_return.success = False
                mongo_return.message = "Failed to insert some records"
                # return False
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def select_all(self, projection=None):
        """
        Returns all documents in a collection

        :param projection: Mongo projection
        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            if not projection:
                projection = dict()
            projection['_id'] = False
            cursor = self.get_collection().find({}, projection)
            result = _cursor_helper(cursor)
            mongo_return.count = len(result)
            mongo_return.success = True
            mongo_return.message = "Query successful"
            mongo_return.documents = result
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def delete(self, seed):
        """
        Delete a single document from a collection. Deletion of a magen_resource that
        does not exist still returns true

        :param seed: Filter of document to be deleted
        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            delete_result = self.get_collection().delete_one(seed)
            mongo_return.success = delete_result.acknowledged
            if delete_result.acknowledged:
                mongo_return.message = "Document deleted"
                mongo_return.count = delete_result.deleted_count
            else:
                mongo_return.message = "Failed to delete document"
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def delete_all(self):
        """
        Delete all the dcouments from collection

        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            result = self.get_collection().delete_many({})
            mongo_return.success = result.acknowledged
            mongo_return.count = result.deleted_count
            if result.acknowledged:
                mongo_return.message = "Documents deleted"
            else:
                mongo_return.message = "Failed to delete documents"
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def find_one_filter(self, seed, projection=None):
        """
        Find a single record by seed and
        remove fields specified in projection

        :param seed: Query filter
        :param projection: Mongo projection
        :rtype: MongoReturn object
        """
        mongo_return = MongoReturn()
        try:
            if not projection:
                projection = dict()
            projection['_id'] = False
            mongo_return.documents = self.get_collection().find_one(seed, projection)
            if mongo_return.documents:
                mongo_return.success = True
                mongo_return.count = 1
            else:
                mongo_return.success = False
                mongo_return.message = "Document not found"
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def replace(self, document_filter, replacement):
        """
        Replace an existing document by another using UUID as key. If document does not exist, create one.
        This function should be used by idempotent REST verbs like PUT.

        :param replacement: The replacement document
        :param document_filter: Mongo document filter with format {"uuid": <document uuid>}
        :rtype: MongoReturn obj
        """
        try:
            replace_result = self.get_collection().find_one_and_replace(document_filter, replacement, upsert=True,
                                                                        return_document=ReturnDocument.AFTER)
            if replace_result and (replace_result.get(self.uuid_field_name, None) == replacement[self.uuid_field_name]):
                mongo_return = MongoReturn(success=True, message="Document replaced", documents=replace_result)
            else:
                mongo_return = MongoReturn(success=False, message="Failed to replace document")
            return mongo_return
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)

    def count_documents(self, document_filter=None):
        """
        Count the number of documents matching a filter

        :param document_filter: Document filter
        :rtype: MongoReturn obj
        """
        mongo_return = MongoReturn()
        try:
            mongo_return.count = self.get_collection().count(document_filter)
        except pymongo.errors.PyMongoError as error:
            return handle_specific_exception(error)
        if mongo_return.count:
            mongo_return.message = "Document found"
            mongo_return.success = True
        else:
            mongo_return.message = "No Documents found"
            mongo_return.success = False
        return mongo_return
