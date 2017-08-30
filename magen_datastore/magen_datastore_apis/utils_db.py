from abc import ABCMeta, abstractmethod
import logging

from magen_logger.logger_config import LogDefaults

#
# Copyright (c) 2015 Cisco Systems, Inc. and others.  All rights reserved.
#

# NO USAGES

__author__ = "rpenno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class IUtils (metaclass=ABCMeta):

    __instance = None
    logger = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls, magen_logger=None):
        if cls.__instance is None:
            cls.logger = magen_logger or logging.getLogger(LogDefaults.default_log_name)
            cls.__instance = cls()
        return cls.__instance

    @abstractmethod
    def check_db(self, db_ip_port):
        pass
