"""Magen Mongo Core Database"""
from magen_datastore_apis.dao_interface import IDao
from magen_datastore_apis.main_db import MainDb
from magen_datastore_apis.utils_db import IUtils
from pymongo import MongoClient

from magen_utils_apis.domain_resolver import LOCAL_MONGO_LOCATOR

__author__ = "repennor@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class MongoCore(MainDb):
    """Magen Mongo Core Database Class"""

    mongo_client = None
    magen_mdb = None
    users = None
    u_groups = None
    clients = None
    policy_contracts = None  # temp - single db for contracts
    policy_sessions = None
    policy_instances = None
    policy_templates = None
    settings = None
    mis_sessions = None
    assets = None

    resource_documents = None

    __instance = None

    def __init__(self):
        super().__init__()
        self.__db_ip_port = LOCAL_MONGO_LOCATOR
        self.__client_strategy = IDao
        self.__user_strategy = IDao
        self.__u_group_strategy = IDao
        self.__utils_strategy = IUtils
        self.__resource_strategy = IDao
        self.__policy_session_strategy = IDao
        self.__policy_instance_strategy = IDao
        self.__policy_contract_strategy = IDao
        self.__policy_template_strategy = IDao
        self.__settings_strategy = IDao
        self.__mis_session_strategy = IDao
        self.__asset_strategy = IDao

    @property
    def asset_strategy(self):
        """DB Element Strategy"""
        return self.__asset_strategy

    @asset_strategy.setter
    def asset_strategy(self, value):
        self.__asset_strategy = value

    @property
    def settings_strategy(self):
        """DB Element Strategy"""
        return self.__settings_strategy

    @settings_strategy.setter
    def settings_strategy(self, value):
        self.__settings_strategy = value

    @property
    def resource_strategy(self):
        """DB Element Strategy"""
        return self.__resource_strategy

    @resource_strategy.setter
    def resource_strategy(self, value):
        self.__resource_strategy = value

    @property
    def user_strategy(self):
        """DB Element Strategy"""
        return self.__user_strategy

    @user_strategy.setter
    def user_strategy(self, value):
        self.__user_strategy = value

    @property
    def client_strategy(self):
        """DB Element Strategy"""
        return self.__client_strategy

    @client_strategy.setter
    def client_strategy(self, value):
        self.__client_strategy = value

    @property
    def u_group_strategy(self):
        """DB Element Strategy"""
        return self.__u_group_strategy

    @u_group_strategy.setter
    def u_group_strategy(self, value):
        self.__u_group_strategy = value

    @property
    def utils_strategy(self):
        """DB Element Strategy"""
        return self.__utils_strategy

    @utils_strategy.setter
    def utils_strategy(self, value):
        self.__utils_strategy = value

    @property
    def policy_template_strategy(self):
        """DB Element Strategy"""
        return self.__policy_template_strategy

    @policy_template_strategy.setter
    def policy_template_strategy(self, value):
        self.__policy_template_strategy = value

    @property
    def policy_instance_strategy(self):
        """DB Element Strategy"""
        return self.__policy_instance_strategy

    @policy_instance_strategy.setter
    def policy_instance_strategy(self, value):
        self.__policy_instance_strategy = value

    @property
    def policy_session_strategy(self):
        """DB Element Strategy"""
        return self.__policy_session_strategy

    @policy_session_strategy.setter
    def policy_session_strategy(self, value):
        self.__policy_session_strategy = value

    @property
    def policy_contract_strategy(self):
        """DB Element Strategy"""
        return self.__policy_contract_strategy

    @policy_contract_strategy.setter
    def policy_contract_strategy(self, value):
        self.__policy_contract_strategy = value

    @property
    def db_ip_port(self):
        """DB Element Strategy"""
        return self.__db_ip_port

    @db_ip_port.setter
    def db_ip_port(self, value):
        self.__db_ip_port = value

    @property
    def mis_session_strategy(self):
        """DB Element Strategy"""
        return self.__mis_session_strategy

    @mis_session_strategy.setter
    def mis_session_strategy(self, value):
        self.__mis_session_strategy = value

    def get_mongo_client(self):
        """Mongo Client Get"""
        return self.mongo_client

    def get_magen_mdb(self):
        """Get Magen Main Db Instance"""
        return self.magen_mdb

    def get_assets(self):
        """Get Assets Colleciton"""
        return self.assets

    def get_policy_templates(self):
        """Get Policy Templates Colleciton"""
        return self.policy_templates

    def get_policy_contracts(self):
        """Get Policy Contracts Colleciton"""
        return self.policy_contracts

    def get_policy_sessions(self):
        """Get Policy Sessions Colleciton"""
        return self.policy_sessions

    def get_policy_instances(self):
        """Get Policy Instances Colleciton"""
        return self.policy_instances

    def get_users(self):
        """Get Users Colleciton"""
        return self.users

    def get_u_groups(self):
        """Get User Groups Colleciton"""
        return self.u_groups

    def get_clients(self):
        """Get Clients Colleciton"""
        return self.clients

    def get_settings(self):
        """Get Settings Colleciton"""
        return self.settings

    def get_resource_documents(self):
        """Get Resource Documents Colleciton"""
        return self.resource_documents

    def get_mis_sessions(self):
        """Get Magen Identity Service Sessions Colleciton"""
        return self.mis_sessions

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def initialize(self):
        self.mongo_client = MongoClient(self.db_ip_port)
        self.magen_mdb = self.mongo_client.get_database('magen')
        # client collections
        self.users = self.magen_mdb.get_collection('users')
        self.u_groups = self.magen_mdb.get_collection('u_groups')
        self.clients = self.magen_mdb.get_collection('clients')
        # policy collections
        self.policy_templates = self.magen_mdb.get_collection('policy_templates')
        self.policy_contracts = self.magen_mdb.get_collection('policy_contracts')
        self.policy_sessions = self.magen_mdb.get_collection('policy_sessions')
        self.policy_instances = self.magen_mdb.get_collection('policy_instances')
        self.resource_documents = self.magen_mdb.get_collection('resource_documents')
        self.settings = self.magen_mdb.get_collection('settings')
        # mis session collections
        self.mis_sessions = self.magen_mdb.get_collection('mis_sessions')
        # asset collections
        self.assets = self.magen_mdb.get_collection('assets')
