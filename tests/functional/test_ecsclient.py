import os
import re
import unittest

import time
from six.moves import configparser
from jsonschema import validate, FormatChecker

from ecsclient.client import Client
from ecsclient.common.exceptions import ECSClientException
from tests.functional import helper
from tests.functional import schemas


class TestFunctional(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFunctional, self).__init__(*args, **kwargs)
        self.skip_tests = False
        self._get_config()

    def _get_config(self):
        config_file = os.environ.get('ECS_TEST_CONFIG_FILE',
                                     '/home/ubuntu/src/test.conf')
        config = configparser.ConfigParser()
        config.read(config_file)
        self.config = config
        if config.has_section('func_test'):
            self.token_endpoint = config.get('func_test', 'token_endpoint')
            self.ecs_endpoint = config.get('func_test', 'ecs_endpoint')
            self.username = config.get('func_test', 'username')
            self.password = config.get('func_test', 'password')
            self.api_version = config.get('func_test', 'api_version')
            license_file = config.get('func_test', 'license_file')
            with open(license_file) as f:
                self.license_text = f.read()
        else:
            self.skip_tests = True

    def _get_client(self):
        return Client(
            self.api_version,
            username=self.username,
            password=self.password,
            ecs_endpoint=self.ecs_endpoint,
            token_endpoint=self.token_endpoint)

    def setUp(self):
        super(TestFunctional, self).setUp()
        if self.skip_tests:
            self.skipTest('SKIPPING FUNCTIONAL TESTS DUE TO NO CONFIG')
        self.client = self._get_client()

    def tearDown(self):
        super(TestFunctional, self).tearDown()

    def assertSameCertificate(self, first, second, msg=None):
        """Fail if the two certificates are not equal.
        """
        first = re.sub(r"\s+", "", first)
        second = re.sub(r"\s+", "", second)
        self.assertEqual(first, second, msg=msg)

    def assertValidSchema(self, object, schema):
        """Fail if the object does not comply with the given schema.
        """
        validate(object, schema, format_checker=FormatChecker())


class TestFunctionalWhoami(TestFunctional):
    def test_whoami(self):
        response = self.client.user_info.whoami()
        self.assertValidSchema(response, schemas.WHOAMI)


class TestFunctionalLicense(TestFunctional):
    def test_get_license(self):
        response = self.client.licensing.get_license()
        self.assertValidSchema(response, schemas.LICENSE)

    def test_add_license(self):
        license = {
            "license_text": self.license_text
        }
        response = self.client.licensing.add_license(license)
        print(response)


class TestFunctionalCertificate(TestFunctional):
    def test_get_certificate(self):
        response = self.client.certificate.get_certificate_chain()
        self.assertValidSchema(response, schemas.CERTIFICATE)

    def test_set_certificate(self):
        # First, set a self-signed certificate
        ip_addresses = ['10.0.0.1']
        response = self.client.certificate.set_certificate_chain(
            selfsigned=True,
            ip_addresses=ip_addresses)
        self.assertValidSchema(response, schemas.CERTIFICATE)

        # Then, provide a private key and a certificate
        private_key = helper.get_sample_private_key()
        certificate = helper.get_sample_certificate()
        response = self.client.certificate.set_certificate_chain(
            private_key=private_key,
            certificate_chain=certificate)
        self.assertValidSchema(response, schemas.CERTIFICATE)
        self.assertSameCertificate(certificate, response['chain'])


class TestFunctionalNamespaces(TestFunctional):
    def __init__(self, *args, **kwargs):
        super(TestFunctionalNamespaces, self).__init__(*args, **kwargs)
        self.namespace_1 = "functional-tests-namespace-%s" % int(time.time())
        self.namespace_2 = self.namespace_1 + '_second'
        self.namespace_3 = self.namespace_1 + '_third'

    def setUp(self):
        super(TestFunctionalNamespaces, self).setUp()
        self.client.namespace.create(self.namespace_1)
        self.client.namespace.create(self.namespace_3)

    def tearDown(self):
        super(TestFunctionalNamespaces, self).tearDown()
        for namespace in [self.namespace_1,
                          self.namespace_2,
                          self.namespace_3]:
            try:
                self.client.namespace.delete(namespace)
            except ECSClientException:
                pass

    def test_namespaces_list(self):
        response = self.client.namespace.list()
        self.assertValidSchema(response, schemas.NAMESPACES)

    def test_namespaces_get_one(self):
        response = self.client.namespace.get(self.namespace_1)
        self.assertValidSchema(response, schemas.NAMESPACE)

    def test_namespaces_update(self):
        # Get the namespace and verify the value of one of its attributes
        response = self.client.namespace.get(self.namespace_1)
        self.assertEqual(response['is_stale_allowed'], False)

        # Update the attribute
        self.client.namespace.update(self.namespace_1, is_stale_allowed=True)

        # Get it again and verify that the value was correctly updated
        response = self.client.namespace.get(self.namespace_1)
        self.assertEqual(response['is_stale_allowed'], True)

    def test_namespaces_create(self):
        response = self.client.namespace.create(self.namespace_2)
        self.assertValidSchema(response, schemas.NAMESPACE)
        self.assertEqual(response['name'], self.namespace_2)

    def test_namespaces_delete(self):
        self.client.namespace.delete(self.namespace_3)
        f = self.client.namespace.get
        self.assertRaises(ECSClientException, f, self.namespace_3)


class TestFunctionalStoragePools(TestFunctional):
    def __init__(self, *args, **kwargs):
        super(TestFunctionalStoragePools, self).__init__(*args, **kwargs)
        self.storage_pool_1 = "functional-tests-storagepool-%s" % int(time.time())
        self.storage_pool_2 = self.storage_pool_1 + '_second'
        self.storage_pool_3 = self.storage_pool_1 + '_third'

    def setUp(self):
        super(TestFunctionalStoragePools, self).setUp()
        r = self.client.storage_pool.create(self.storage_pool_1)
        self.storage_pool_1_id = r['id']
        self.storage_pool_2_id = 'placeholder'
        r = self.client.storage_pool.create(self.storage_pool_3)
        self.storage_pool_3_id = r['id']

    def tearDown(self):
        super(TestFunctionalStoragePools, self).tearDown()
        for storage_pool_id in [self.storage_pool_1_id,
                                self.storage_pool_2_id,
                                self.storage_pool_3_id]:
            try:
                self.client.storage_pool.delete(storage_pool_id)
            except ECSClientException:
                pass

    def test_storage_pools_list(self):
        response = self.client.storage_pool.list()
        self.assertValidSchema(response, schemas.STORAGE_POOLS)

    def test_storage_pools_get_one(self):
        response = self.client.storage_pool.get(self.storage_pool_1_id)
        self.assertValidSchema(response, schemas.STORAGE_POOL)

    def test_storage_pools_create(self):
        response = self.client.storage_pool.create(self.storage_pool_2)
        self.assertValidSchema(response, schemas.STORAGE_POOL)
        self.assertEqual(response['name'], self.storage_pool_2)

    def test_storage_pools_update(self):
        new_name = self.storage_pool_1 + '-updated'
        # Get the namespace and verify the value of one of its attributes
        response = self.client.storage_pool.get(self.storage_pool_1_id)
        self.assertNotEqual(response['name'], new_name)
        self.assertFalse(response['isProtected'])
        self.assertFalse(response['isColdStorageEnabled'])

        # Update the attribute and check the response
        response = self.client.storage_pool.update(self.storage_pool_1_id,
                                                   name=new_name,
                                                   is_protected=True)
        self.assertEqual(response['name'], new_name)
        self.assertTrue(response['isProtected'])

    def test_storage_pools_delete(self):
        self.client.storage_pool.delete(self.storage_pool_3_id)
        f = self.client.storage_pool.get
        self.assertRaises(ECSClientException, f, self.storage_pool_3_id)
