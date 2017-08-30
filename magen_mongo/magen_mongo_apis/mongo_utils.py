#
# Copyright (c) 2015 Cisco Systems, Inc. and others.  All rights reserved.
#

import sys

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from magen_datastore_apis.utils_db import IUtils
from .mongo_return import MongoReturn

author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class MongoUtils(IUtils):

    @staticmethod
    def respond(success, response):
        return {"success": success, "response": response}

    def check_db(self, db_ip_port):
        """
        We test Mongo Server right off the bat and if it is not working we raise and error and exit
        """
        try:
            client = MongoClient(db_ip_port)
            client.server_info()
        except (ConnectionFailure, ServerSelectionTimeoutError) as err:
            self.logger.error("Could not connect to Mongo Server, message: %s" % err)
            sys.exit(0)

    @staticmethod
    def check_bulk_operation_result(bulk_result):
        mongo_return = MongoReturn()
        write_error_list = bulk_result["writeErrors"]
        if len(write_error_list):
            mongo_return.success = False
        else:
            mongo_return.success = True
        return mongo_return
