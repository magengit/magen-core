"""Monkey Patch for Handling PyMongo Exceptions"""
import logging
import sys
from functools import singledispatch
from pprint import pprint

import pymongo
from magen_logger.logger_config import LogDefaults
from .mongo_return import MongoReturn

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


@singledispatch
def handle_specific_exception(err):
    """
    Handles exceptions for the PyMongo APIs functions. This function is overloaded with specific functions
    for the most important types of exceptions

    :rtype: Rest return object
    """
    logger = logging.getLogger(LogDefaults.default_log_name)
    logger.error('Unexpected PyMongo Error. Error: %s', sys.exc_info()[0])
    success = False
    message = err.args[0]
    mongo_return_obj = MongoReturn(success=success, message=message)

    return mongo_return_obj


@handle_specific_exception.register(pymongo.errors.OperationFailure)
def operation_failure(err):
    """Handles specific exception pymongo.errors.OperationFailure"""
    success = False
    message = err.details
    mongo_return_obj = MongoReturn(success=success, message=message, db_exception=err, code=err.code)
    return mongo_return_obj


@handle_specific_exception.register(pymongo.errors.NetworkTimeout)
def network_timeout(err):
    """Handles specific exception pymongo.errors.NetworkTimeout"""
    success = False
    message = err.args[0]
    mongo_return_obj = MongoReturn(success=success, message=message, db_exception=err)
    return mongo_return_obj


@handle_specific_exception.register(pymongo.errors.ExecutionTimeout)
def execution_timeout(err):
    """Handles specific exception pymongo.errors.ExecutionTimeout"""
    success = False
    message = err.args[0]
    mongo_return_obj = MongoReturn(success=success, message=message, db_exception=err)
    return mongo_return_obj


@handle_specific_exception.register(pymongo.errors.CursorNotFound)
def cursor_not_found(err):
    """Handles specific exception pymongo.errors.CursorNotFound"""
    success = False
    message = err.args[0]
    mongo_return_obj = MongoReturn(success=success, message=message, db_exception=err)
    return mongo_return_obj


@handle_specific_exception.register(pymongo.errors.PyMongoError)
def pymongo_error(err):
    """Handles specific exception pymongo.errors.NetworkTimeout"""
    success = False
    message = "PyMongo Error"
    mongo_return_obj = MongoReturn(success=success, message=message, db_exception=err)
    return mongo_return_obj


@handle_specific_exception.register(pymongo.errors.BulkWriteError)
def bulk_write_error(err):
    """Handles specific exception pymongo.errors.BulkWriteError"""
    success = False
    message = "BulkWriteError"
    pprint(err.details)
    mongo_return_obj = MongoReturn(success=success, message=message, db_exception=err)
    return mongo_return_obj
