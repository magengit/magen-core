#! /usr/bin/python3
import unittest
from magen_utils_apis import domain_resolver
import os

import magen_core_test_env

__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__email__ = "alifar@cisco.com"
__data__ = "04/05/2017"


class TestDomainResolver(unittest.TestCase):
    """
    Tests for domain_resolver.py
    Execute 'make test' from magen_core directory
    """
    test_no_magen_domain_file_path = os.path.abspath('tests/data/domain_resolver-no_magen_domain_file')
    test_dev_domain_file_path = os.path.abspath('tests/data/domain_resolver-dev_domain_file')
    test_staging_domain_file_path = os.path.abspath('tests/data/domain_resolver-staging_domain_file')
    test_no_domain_file_path = os.path.abspath('tests/data/domain_resolver-no_domain_file')
    test_domain_line_alt_start_file = os.path.abspath('tests/data/domain_resolver-domain_line_alt_start_file')

    def test_NoMagenDomainFile(self):
        test_domain = domain_resolver.parse_resolv(TestDomainResolver.test_no_magen_domain_file_path)
        self.assertEquals(test_domain, 'localhost')

    def test_DevDomainFile(self):
        test_domain = domain_resolver.parse_resolv(TestDomainResolver.test_dev_domain_file_path)
        self.assertEquals(test_domain, 'dev.magen.io')

    def test_StagingDomainFile(self):
        test_domain = domain_resolver.parse_resolv(TestDomainResolver.test_staging_domain_file_path)
        self.assertEquals(test_domain, 'staging.magen.io')

    def test_FileDoesNotExist(self):
        test_domain = domain_resolver.parse_resolv("file_not_exist")
        self.assertEquals(test_domain, 'localhost')

    def test_NoDomainFile(self):
        test_domain = domain_resolver.parse_resolv(TestDomainResolver.test_no_domain_file_path)
        self.assertEquals(test_domain, 'localhost')

    def test_DomainLineAltStart(self):
        test_domain = domain_resolver.parse_resolv(TestDomainResolver.test_domain_line_alt_start_file)
        self.assertEquals(test_domain, 'localhost')

    def test_DynamicDomainUpdate(self):
        test_domain = domain_resolver.parse_resolv(TestDomainResolver.test_dev_domain_file_path)
        self.assertEquals(test_domain, 'dev.magen.io')
        test_domain = domain_resolver.parse_resolv(TestDomainResolver.test_staging_domain_file_path)
        self.assertEquals(test_domain, 'staging.magen.io')

    def test_mongo_host_port(self):
        magen_mongo, mongo_port = domain_resolver.mongo_host_port()
        self.assertEquals(magen_mongo, '127.0.0.1')
        self.assertEquals(mongo_port, 27017)

    def test_mongo_locator(self):
        test_mongo = domain_resolver.mongo_locator()
        self.assertEquals(test_mongo, '127.0.0.1:27017')
