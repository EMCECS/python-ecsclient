import os
import re
import unittest

import time
from six.moves import configparser
from jsonschema import validate, FormatChecker

from ecsclient.client import Client
from tests.functional import helper
from tests.functional import schemas


class TestFunctional(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFunctional, self).__init__(*args, **kwargs)
        self.skip_tests = False
        self._get_config()

    def assertSameCertificate(self, first, second, msg=None):
        """Fail if the two certificates are not equal.
        """
        first = re.sub(r"\s+", "", first)
        second = re.sub(r"\s+", "", second)
        self.assertEqual(first, second, msg=msg)

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

    def _validate_response(self, response, schema):
        validate(response, schema, format_checker=FormatChecker())

    def test_whoami(self):
        schema = {
            "type": "object",
            "properties": {
                "namespace": {"type": "string"},
                "last_time_password_changed": {
                    "type": "string",
                    "format": "date-time"
                },
                "distinguished_name": {"type": "string"},
                "common_name": {"type": "string"},
                "roles": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1
                    },
                    "minItems": 1,
                    "uniqueItems": True
                }
            },
            "required": [
                "namespace",
                "last_time_password_changed",
                "distinguished_name",
                "common_name",
                "roles",
            ]
        }
        response = self.client.user_info.whoami()
        self._validate_response(response, schema)

    def test_get_license(self):
        schema = {
            "type": "object",
            "properties": {
                "license_feature": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "properties": {
                            "product": {"type": "string"},
                            "version": {"type": "string"},
                            "model": {"type": "string"},
                            "licensed_ind": {"type": "boolean"},
                            "trial_license_ind": {"type": "boolean"},
                            "storage_capacity": {"type": "string"},
                            "notice": {"type": "string"},
                            "serial": {"type": "string"},
                            "expired_ind": {"type": "boolean"},
                            "issued_date": {"type": "string", "format": "date-time"},
                            "license_id_indicator": {"type": "string"},
                            "issuer": {"type": "string"},
                            "site_id": {"type": "string"}
                        },
                        "required": [
                            "product",
                            "version",
                            "model",
                            "licensed_ind",
                            "trial_license_ind",
                            "storage_capacity",
                            "notice",
                            "serial",
                            "expired_ind",
                            "issued_date",
                            "license_id_indicator",
                            "issuer",
                            "site_id"
                        ]
                    },
                },
                "license_text": {"type": "string"}
            },
            "required": [
                "license_feature",
                "license_text"
            ]
        }
        response = self.client.licensing.get_license()
        self._validate_response(response, schema)

    def test_add_license(self):
        license = {
            "license_text": self.license_text
        }
        response = self.client.licensing.add_license(license)
        print(response)

    def test_get_certificate(self):
        schema = {
            "type": "object",
            "properties": {
                "chain": {"type": "string"}
            },
            "required": [
                "chain",
            ]
        }
        response = self.client.certificate.get_certificate_chain()
        self._validate_response(response, schema)

    def test_set_certificate_selfsigned(self):
        schema = {
            "type": "object",
            "properties": {
                "chain": {"type": "string"}
            },
            "required": [
                "chain",
            ]
        }
        ip_addresses = ['10.0.0.1']
        response = self.client.certificate.set_certificate_chain(
            selfsigned=True,
            ip_addresses=ip_addresses)
        self._validate_response(response, schema)

    def test_set_certificate_provided(self):
        schema = {
            "type": "object",
            "properties": {
                "chain": {"type": "string"}
            },
            "required": [
                "chain",
            ]
        }
        private_key = helper.get_sample_private_key()
        certificate = helper.get_sample_certificate()
        response = self.client.certificate.set_certificate_chain(
            private_key=private_key,
            certificate_chain=certificate)
        self._validate_response(response, schema)
        self.assertSameCertificate(certificate, response['chain'])

    def test_namespaces(self):

        # Get all namespaces
        response = self.client.namespace.get_namespaces()
        self._validate_response(response, schemas.NAMESPACES)

        # Get the first namespace returned individually
        namespace_id = response['namespace'][0]['id']
        response = self.client.namespace.get_namespace(namespace_id)
        self._validate_response(response, schemas.NAMESPACE)

        # Crete a new namespace
        namespace_name = "functional-tests-namespace-%s" % int(time.time())
        response = self.client.namespace.create_namespace(namespace_name, is_stale_allowed=False)
        self._validate_response(response, schemas.NAMESPACE)
        self.assertEqual(response['is_stale_allowed'], False)

        # Update a namespace
        namespace_id = response['id']
        self.client.namespace.update_namespace(namespace_id, is_stale_allowed=True)
        response = self.client.namespace.get_namespace(namespace_id)
        self.assertEqual(response['is_stale_allowed'], True)

        # TODO: Delete namespace

