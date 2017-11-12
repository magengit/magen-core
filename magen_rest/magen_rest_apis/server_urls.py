"""Server Urls Class"""
import logging

from magen_utils_apis import domain_resolver

from magen_logger.logger_config import LogDefaults

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


DEFAULT_DOMAIN = 'localhost'


class ServerUrls(object):
    """
    Server Urls is a single source of hosts and ports for all of Magen Services.

    It manages domains for Magen services, including AWS Load Balancer domain, docker and localhost
    """
    __instance = None
    ingestion_port = 5020
    identity_port = 5030
    key_port = 5010
    policy_port = 5000
    location_port = 5003

    ingestion_server_name = 'is'
    identity_server_name = 'id'
    key_server_name = 'ks'
    policy_server_name = 'ps'
    location_server_name = 'ps'

    ingestion_docker_name = 'magen_ingestion'
    identity_docker_name = 'magen_id_service'
    key_docker_name = 'magen_ks'
    policy_docker_name = 'magen_policy'
    location_docker_name = 'magen_policy'

    def __init__(self, default_domain_name=None, magen_logger=None):
        """
        Init domain for ServerUrls by resolving
        if the service is located on AWS domain, inside the docker or on local machine

        :param default_domain_name: alternative domain name to be used
        :type default_domain_name: str

        :param magen_logger: Magen Logger
        """

        self.__domain_name = default_domain_name or domain_resolver.parse_resolv()

        self.logger = magen_logger or logging.getLogger(LogDefaults.default_log_name)

        self.__disable_url_host_port = "0.0.0.0:0"

        self.__put_json_headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        self.__get_json_headers = {'Accept': 'application/json'}

        self.__post_xml_headers = {
            'content-type': 'application/xml',
            'Accept': 'application/xml'}
        self.__get_xml_headers = {'Accept': 'application/xml'}

        # IDENTITY
        self.__identity_server_url_host_port = None
        self.__identity_server_base_url = None

        # INGESTION
        self.__ingestion_server_url_host_port = None
        self.__ingestion_server_base_url = None
        self.__ingestion_server_assets_url = None
        self.__ingestion_server_asset_url = None
        self.__ingestion_server_single_asset_url = None
        self.__ingestion_server_upload_url = None
        self.__ingestion_server_check_url = None

        # KEY Server
        self.__key_server_url_host_port = None
        self.__key_server_base_url = None
        self.__key_server_asset_keys_url = None
        self.__key_server_asset_keys_keys_url = None
        self.__key_server_asset_keys_keys_key_url = None
        self.__key_server_assets_url = None
        self.__key_server_asset_url = None
        self.__key_server_single_asset_url = None

        # POLICY
        self.__policy_server_url_host_port = None
        self.__policy_server_base_url = None
        self.__policy_server_base_url_new = None
        self.__policy_full_reset_url = None
        self.__policy_templates_url = None
        self.__policy_template_url = None
        self.__policy_single_template_url = None
        self.__policy_contracts_url = None
        self.__policy_contract_url = None
        self.__policy_single_contract_url = None
        self.__policy_sessions_url = None
        self.__policy_session_url = None
        self.__policy_single_session_url = None
        self.__policy_instances_url = None
        self.__policy_validation_base_url = None
        self.__policy_validate_asset_access_url = None
        self.__policy_mock_location_update_url = None

        # LOCATION
        self.__location_server_url_host_port = None
        self.__location_server_base_url = None
        self.__location_stores_url = None
        self.__location_server_host_base_url = None

        self.set_domain_ports()

    def _set_domain_ports_default(self):
        """
        Set default domain (localhost) and default ports

        :rtype: void
        """
        self.set_ingestion_server_url_host_port("{}:{}".format(self.domain_name, ServerUrls.ingestion_port))
        self.set_identity_server_url_host_port("{}:{}".format(self.domain_name, ServerUrls.identity_port))
        self.set_key_server_url_host_port("{}:{}".format(self.domain_name, ServerUrls.key_port))
        self.set_policy_server_url_host_port("{}:{}".format(self.domain_name, ServerUrls.policy_port))
        self.set_location_server_url_host_port("{}:{}".format(self.domain_name, ServerUrls.location_port))

    def _set_domain_ports_docker(self):
        """
        Set specific docker names as domain and default ports

        :rtype: void
        """
        self.set_ingestion_server_url_host_port("{}:{}".format(ServerUrls.ingestion_docker_name, ServerUrls.ingestion_port))
        self.set_identity_server_url_host_port("{}:{}".format(ServerUrls.identity_docker_name, ServerUrls.identity_port))
        self.set_key_server_url_host_port("{}:{}".format(ServerUrls.key_docker_name, ServerUrls.key_port))
        self.set_policy_server_url_host_port("{}:{}".format(ServerUrls.policy_docker_name, ServerUrls.policy_port))
        self.set_location_server_url_host_port("{}:{}".format(ServerUrls.location_docker_name, ServerUrls.location_port))

    def _set_domain_ports_aws(self):
        """
        Set AWS Magen domain name and default 80 or 443 ports

        :rtype: void
        """
        self.set_ingestion_server_url_host_port("{}.{}".format(ServerUrls.ingestion_server_name, self.domain_name))
        self.set_identity_server_url_host_port("{}.{}".format(ServerUrls.identity_server_name, self.domain_name))
        self.set_key_server_url_host_port("{}.{}".format(ServerUrls.key_server_name, self.domain_name))
        self.set_policy_server_url_host_port("{}.{}".format(ServerUrls.policy_server_name, self.domain_name))
        # FIXME: Location is set to localhost by default for now
        # self.set_location_server_url_host_port("{}.{}".format(ServerUrls.location_server_name, self.domain_name))
        self.set_location_server_url_host_port("localhost:{}".format(self.location_port))

    def set_domain_ports(self):
        """
        Set domains depending on environment set up

        :rtype: void
        """
        if self.domain_name == DEFAULT_DOMAIN:
            self._set_domain_ports_docker() if domain_resolver.inside_docker() else self._set_domain_ports_default()
        else:
            self._set_domain_ports_aws()

    @property
    def domain_name(self):
        """Domain Name"""
        return self.__domain_name

    @domain_name.setter
    def domain_name(self, value):
        self.__domain_name = value
        self.set_domain_ports()

    @property
    def disable_url_host_port(self):
        """Default Disabled URL Host Port"""
        return self.__disable_url_host_port

    @property
    def put_json_headers(self):
        return self.__put_json_headers

    @put_json_headers.setter
    def put_json_headers(self, value):
        self.__put_json_headers = value

    @property
    def get_json_headers(self):
        """GET JSON Headers"""
        return self.__get_json_headers

    @get_json_headers.setter
    def get_json_headers(self, value):
        self.__get_json_headers = value

    def set_ingestion_server_url_host_port(self, ingestion_server_url_host_port):
        self.__ingestion_server_url_host_port = ingestion_server_url_host_port
        self.__ingestion_server_base_url = "http://" + self.__ingestion_server_url_host_port + "/magen/ingestion/v2/"
        self.__ingestion_server_assets_url = self.__ingestion_server_base_url + "assets/"
        self.__ingestion_server_asset_url = self.__ingestion_server_assets_url + "asset/"
        self.__ingestion_server_single_asset_url = self.__ingestion_server_asset_url + "{}/"
        self.__ingestion_server_upload_url = self.__ingestion_server_base_url + "upload/"
        self.__ingestion_server_check_url = self.__ingestion_server_base_url + "check/"

    def set_identity_server_url_host_port(self, identity_server_url_host_port):
        self.logger.debug("set_identity_server_url_host_port: %s", identity_server_url_host_port)

        self.__identity_server_url_host_port = identity_server_url_host_port
        self.__identity_server_base_url = "http://" + self.__identity_server_url_host_port + "/magen/id/v2/"

    def set_key_server_url_host_port(self, key_server_url_host_port):

        self.__key_server_url_host_port = key_server_url_host_port
        self.__key_server_base_url = "http://" + self.__key_server_url_host_port + "/magen/ks/v3/"
        self.__key_server_asset_keys_url = self.key_server_base_url + "asset_keys/"
        self.__key_server_asset_keys_keys_url = self.__key_server_asset_keys_url + "keys/"
        self.__key_server_asset_keys_keys_key_url = self.__key_server_asset_keys_keys_url + "key/"
        self.__key_server_assets_url = self.__key_server_asset_keys_url + "assets/"
        self.__key_server_asset_url = self.__key_server_assets_url + "asset/"
        self.__key_server_single_asset_url = self.__key_server_asset_url + "{}/"

    def set_policy_server_url_host_port(self, policy_server_ip_port):

        self.__policy_server_url_host_port = policy_server_ip_port

        self.__policy_server_base_url = "http://" + self.__policy_server_url_host_port + "/magen/policy/v2/"

        self.__policy_full_reset_url = self.__policy_server_base_url + "full_reset/"

        self.__policy_templates_url = self.__policy_server_base_url + "templates/"

        self.__policy_template_url = self.__policy_templates_url + "template/"

        self.__policy_single_template_url = self.__policy_template_url + "{}/"

        self.__policy_contracts_url = self.__policy_server_base_url + "contracts/"

        self.__policy_contract_url = self.__policy_contracts_url + "contract/"

        self.__policy_single_contract_url = self.__policy_contract_url + "{}/"

        self.__policy_sessions_url = self.__policy_server_base_url + "sessions/"

        self.__policy_session_url = self.__policy_sessions_url + "session/"

        self.__policy_single_session_url = self.__policy_session_url + "{}/"

        self.__policy_instances_url = self.__policy_server_base_url + "instances/"

        self.__policy_validation_base_url = self.__policy_server_base_url + "validation/"

        self.__policy_validate_asset_access_url = (
            self.__policy_validation_base_url + "asset/{}/")

        self.__policy_mock_location_update_url = self.__policy_server_base_url + "magen_debug/location_update"

    def set_location_server_url_host_port(self, location_server_url_host_port):
        self.logger.debug("set_location_server_url_host_port: %s", location_server_url_host_port)

        self.__location_server_url_host_port = location_server_url_host_port
        self.__location_server_host_base_url = "http://" + self.__location_server_url_host_port + "/"
        self.__location_server_base_url = self.__location_server_host_base_url + "magen/location/v2/"
        self.__location_stores_url = self.__location_server_base_url + "stores/"

    @property
    def ingestion_server_url_host_port(self):
        return self.__ingestion_server_url_host_port

    @ingestion_server_url_host_port.setter
    def ingestion_server_url_host_port(self, value):
        pass

    @property
    def ingestion_server_upload_url(self):
        return self.__ingestion_server_upload_url

    @ingestion_server_upload_url.setter
    def ingestion_server_upload_url(self, value):
        pass

    @property
    def ingestion_server_check_url(self):
        return self.__ingestion_server_check_url

    @ingestion_server_check_url.setter
    def ingestion_server_check_url(self, value):
        pass

    @property
    def ingestion_server_base_url(self):
        return self.__ingestion_server_base_url

    @ingestion_server_base_url.setter
    def ingestion_server_base_url(self, value):
        pass

    @property
    def ingestion_server_assets_url(self):
        return self.__ingestion_server_assets_url

    @ingestion_server_assets_url.setter
    def ingestion_server_assets_url(self, value):
        pass

    @property
    def ingestion_server_asset_url(self):
        return self.__ingestion_server_asset_url

    @ingestion_server_asset_url.setter
    def ingestion_server_asset_url(self, value):
        pass

    @property
    def ingestion_server_single_asset_url(self):
        return self.__ingestion_server_single_asset_url

    @ingestion_server_single_asset_url.setter
    def ingestion_server_single_asset_url(self, value):
        pass

    @property
    def identity_server_url_host_port(self):
        return self.__identity_server_url_host_port

    @property
    def identity_server_base_url(self):
        return self.__identity_server_base_url

    @property
    def key_server_url_host_port(self):
        return self.__key_server_url_host_port

    @property
    def key_server_base_url(self):
        return self.__key_server_base_url

    @property
    def key_server_asset_keys_keys_key_url(self):
        return self.__key_server_asset_keys_keys_key_url

    @key_server_asset_keys_keys_key_url.setter
    def key_server_asset_keys_keys_key_url(self, value):
        self.__key_server_asset_keys_keys_key_url = value

    @property
    def key_server_asset_keys_keys_url(self):
        return self.__key_server_asset_keys_keys_url

    @key_server_asset_keys_keys_url.setter
    def key_server_asset_keys_keys_url(self, value):
        self.__key_server_asset_keys_keys_url = value

    @property
    def key_server_assets_url(self):
        return self.__key_server_assets_url

    @key_server_assets_url.setter
    def key_server_assets_url(self, value):
        self.__key_server_assets_url = value

    @property
    def key_server_asset_url(self):
        return self.__key_server_asset_url

    @key_server_asset_url.setter
    def key_server_asset_url(self, value):
        self.__key_server_asset_url = value

    @property
    def key_server_single_asset_url(self):
        return self.__key_server_single_asset_url

    @property
    def policy_server_base_url(self):
        return self.__policy_server_base_url

    @property
    def policy_server_url_host_port(self):
        return self.__policy_server_url_host_port

    @property
    def policy_full_reset_url(self):
        return self.__policy_full_reset_url

    @policy_full_reset_url.setter
    def policy_full_reset_url(self, value):
        self.__policy_full_reset_url = value

    @property
    def policy_templates_url(self):
        return self.__policy_templates_url

    @policy_templates_url.setter
    def policy_templates_url(self, value):
        self.__policy_contracts_url = value

    @property
    def policy_template_url(self):
        return self.__policy_template_url

    @policy_template_url.setter
    def policy_template_url(self, value):
        self.__policy_template_url = value

    @property
    def policy_single_template_url(self):
        return self.__policy_single_template_url

    @policy_single_template_url.setter
    def policy_single_template_url(self, value):
        self.__policy_single_template_url = value

    @property
    def policy_contracts_url(self):
        return self.__policy_contracts_url

    @policy_contracts_url.setter
    def policy_contracts_url(self, value):
        self.__policy_contracts_url = value

    @property
    def policy_contract_url(self):
        return self.__policy_contract_url

    @policy_contract_url.setter
    def policy_contract_url(self, value):
        self.__policy_contract_url = value

    @property
    def policy_single_contract_url(self):
        return self.__policy_single_contract_url

    @policy_single_contract_url.setter
    def policy_single_contract_url(self, value):
        self.__policy_single_contract_url = value

    @property
    def policy_sessions_url(self):
        return self.__policy_sessions_url

    @property
    def policy_session_url(self):
        return self.__policy_session_url

    @policy_session_url.setter
    def policy_session_url(self, value):
        self.__policy_session_url = value

    @property
    def policy_single_session_url(self):
        return self.__policy_single_session_url

    @property
    def policy_instances_url(self):
        return self.__policy_instances_url

    @policy_instances_url.setter
    def policy_instances_url(self, value):
        self.__policy_instances_url = value

    @property
    def policy_validation_base_url(self):
        return self.__policy_validation_base_url

    @policy_validation_base_url.setter
    def policy_validation_base_url(self, value):
        self.__policy_validation_base_url = value

    @property
    def policy_validate_asset_access_url(self):
        return self.__policy_validate_asset_access_url

    @property
    def location_server_host_base_url(self):
        return self.__location_server_host_base_url

    @property
    def location_server_base_url(self):
        return self.__location_server_base_url

    @property
    def location_server_url_host_port(self):
        return self.__location_server_url_host_port

    # deprecate(?)
    @property
    def policy_mock_location_update_url(self):
        return self.__policy_mock_location_update_url

    @policy_mock_location_update_url.setter
    def location_update_url(self, value):
        self.__policy_mock_location_update_url = value

    @property
    def location_stores_url(self):
        return self.__location_stores_url

    @location_stores_url.setter
    def location_stores_url(self, value):
        self.__location_stores_url = value

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
