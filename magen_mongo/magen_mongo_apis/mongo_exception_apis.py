import logging
import sys
from functools import singledispatch
from pprint import pprint

import pymongo
from magen_logger.logger_config import LogDefaults
from magen_utils_apis.singleton_meta import Singleton

from .mongo_return import MongoReturn

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class MongoExceptionApis(metaclass=Singleton):

    @singledispatch
    def handle_specific_exception(e):
        """
        Handles exceptions for the REST APIs functions. This function is overloaded with specific functions
        for the most important types of exceptions

        :rtype: Rest return object
        """
        logger = logging.getLogger(LogDefaults.default_log_name)
        logger.error('Unexpected Error. Error: %s', sys.exc_info()[0])
        success = False
        message = e.args[0]
        mongo_return_obj = MongoReturn(success=success, message=message)

        return mongo_return_obj

    @handle_specific_exception.register(pymongo.errors.OperationFailure)
    def _(e):
        success = False
        mongo_status = e.code
        message = e.details
        mongo_return_obj = MongoReturn(success=success, message=message, db_exception=e)
        return mongo_return_obj

    @handle_specific_exception.register(pymongo.errors.NetworkTimeout)
    def _(e):
        success = False
        message = e.args[0]
        mongo_return_obj = MongoReturn(success=success, message=message, db_exception=e)
        return mongo_return_obj

    @handle_specific_exception.register(pymongo.errors.ExecutionTimeout)
    def _(e):
        success = False
        message = e.args[0]
        mongo_return_obj = MongoReturn(success=success, message=message, db_exception=e)
        return mongo_return_obj

    @handle_specific_exception.register(pymongo.errors.CursorNotFound)
    def _(e):
        success = False
        message = e.args[0]
        mongo_return_obj = MongoReturn(success=success, message=message, db_exception=e)
        return mongo_return_obj

    @handle_specific_exception.register(pymongo.errors.PyMongoError)
    def _(e):
        success = False
        message = "PyMongo Error"
        mongo_return_obj = MongoReturn(success=success, message=message, db_exception=e)
        return mongo_return_obj

    @handle_specific_exception.register(pymongo.errors.BulkWriteError)
    def _(e):
        success = False
        message = "BulkWriteError"
        pprint(e.details)
        mongo_return_obj = MongoReturn(success=success, message=message, db_exception=e)
        return mongo_return_obj
