#! /bin/usr/python3
"""Server Urls Test Suite"""
import unittest
from unittest.mock import patch
from magen_rest.magen_rest_apis.server_urls import ServerUrls

__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__email__ = "alifar@cisco.com"
__date__ = "04/07/2017"
__version__ = "0.1"
__status__ = "alpha"


class TestServerUrls(unittest.TestCase):
    """Server Urls Test"""
    services = ['ingestion', 'key', 'identity', 'policy']
    server_names = ['is', 'ks', 'id', 'ps']
    pattern = 'server_url_host_port'
    staging_domain = 'staging.magen.io'
    dev_domain = 'dev.magen.io'
    localhost = 'localhost'
    ports = [5020, 5010, 5030, 5000]
    location_host_port = "localhost:5003"

    def assert_helper(self, server_urls, domain, ports=True):
        """
        This method is resolving available attributed from ServerUrl and checks them for domain and ports
        :param domain: string - domain_name
        :param ports: boolean - depending on domain_name we expect of usage TestServerUrls.ports or port 80
        :return: void
        """
        print("Domain Names: ")

        for index, service in enumerate(TestServerUrls.services):
            host_port_property = getattr(server_urls, TestServerUrls.pattern) if not service else \
                getattr(server_urls, "{}_{}".format(service, TestServerUrls.pattern))
            print("{}:".format(service), host_port_property)
            if ports:
                self.assertEquals(host_port_property, "{}:{}".format(domain, TestServerUrls.ports[index]))
            else:
                self.assertEquals(host_port_property, "{}.{}".format(TestServerUrls.server_names[index], domain))
        print("location", server_urls.location_server_url_host_port)
        self.assertEquals(server_urls.location_server_url_host_port, TestServerUrls.location_host_port)

    @patch.object(ServerUrls, 'domain_name', localhost)
    def test_LocalhostPortsSet(self):
        """
        This method checks whether 'localhost' domain_name is properly assigned to all services
        :return: void
        """
        print()
        print("========== Test Localhost Domain and Ports set ==========")
        self.assert_helper(server_urls=ServerUrls(), domain=TestServerUrls.localhost)

    @patch.object(ServerUrls, 'domain_name', staging_domain)
    def test_StagingDomainPortsSet(self):
        """
        This method checks whether 'staging.domain.io' domain_name is properly assigned to all services
        :return: void
        """
        print()
        print("========== Test Staging Domain and Ports set ==========")
        self.assert_helper(server_urls=ServerUrls(), domain=TestServerUrls.staging_domain, ports=False)

    @patch.object(ServerUrls, 'domain_name', dev_domain)
    def test_DevDomainPortsSet(self):
        """
        This method checks whether 'localhost' domain_name is properly assigned to all services
        :return: void
        """
        print()
        print("========== Test Dev Domain and Ports set ==========")
        self.assert_helper(server_urls=ServerUrls(), domain=TestServerUrls.dev_domain, ports=False)

    def test_DynamicDomainUpdate(self):
        """
        This method checks whether domain_name property update affects all services
        :return: void
        """
        print()
        print("========== Test Dynamic Domain Update ==========")
        test_domain_name = "test_domain_name"
        server_urls = ServerUrls()
        default_domain_name = server_urls.domain_name
        server_urls.domain_name = test_domain_name
        self.assert_helper(server_urls, domain=test_domain_name, ports=False)
        server_urls.domain_name = default_domain_name
