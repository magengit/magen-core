# !/bin/usr/python3

from magen_mongo_apis.concrete_dao import Dao
from .magen_test_db import MagenTestDb

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class MagenTestDbStrategy(Dao):

    def get_collection(self):
        mongo_test_db = MagenTestDb.get_instance()
        return mongo_test_db.magen_test_collection

