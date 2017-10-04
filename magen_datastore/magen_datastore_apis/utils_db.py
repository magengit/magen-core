from abc import ABCMeta, abstractmethod
import logging

from magen_logger.logger_config import LogDefaults

__author__ = "rpenno"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class IUtils (metaclass=ABCMeta):
    """Utils Db Singleton Interface"""

    __instance = None
    logger = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls, magen_logger=None):
        """Instance """
        if cls.__instance is None:
            cls.logger = magen_logger or logging.getLogger(LogDefaults.default_log_name)
            cls.__instance = cls()
        return cls.__instance

    @abstractmethod
    def check_db(self, db_ip_port):
        """Abstract method to check Database connection"""
        pass
