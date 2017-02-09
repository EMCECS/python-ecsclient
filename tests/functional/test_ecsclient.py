import os
import unittest

from six.moves import configparser
from jsonschema import validate, FormatChecker

from ecsclient.client import Client


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
