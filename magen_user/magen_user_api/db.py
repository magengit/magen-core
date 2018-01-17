# coding=utf-8
"""
Db Connection Configuration and Context Manager
"""

import pymongo
from contextlib import contextmanager

__copyright__ = "Copyright(c) 2018, Cisco Systems, Inc."
__status__ = "alpha"


@contextmanager
def connect(db_name, host='localhost', port=27017, **kwargs):
    """
    Context Manger for Mongo Database Connection
    :param db_name: name for DB for connection establishment
    :type db_name: str
    :param host: Mongo Server host
    :type host: str
    :param port: Mongo Server port
    :type port: int
    :param kwargs: other arguments
    :return: generator with Mongo Collection object

    .. note:: username={value} and password={value} must be provided in kwargs for secure connection
    """
    m_client = pymongo.MongoClient(host, port, **kwargs)
    try:
        db_instance = m_client.get_database(db_name)
        yield db_instance
    finally:
        m_client.close()
