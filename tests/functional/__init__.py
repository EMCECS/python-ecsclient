import os
import re
import unittest

from six.moves import configparser

from ecsclient.client import Client
from ecsclient.common.util import is_valid_response


class BaseTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.skip_tests = False
        self._get_config()

    def _get_config(self):
        config_file = os.environ.get('ECS_TEST_CONFIG_FILE',
                                     os.path.join(os.getcwd(), "tests/test.conf"))
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
            self.override_header = config.get("func_test", 'override_header')
        else:
            self.skip_tests = True

    def _get_client(self):
        return Client(
            self.api_version,
            username=self.username,
            password=self.password,
            ecs_endpoint=self.ecs_endpoint,
            token_endpoint=self.token_endpoint,
            override_header=self.override_header)

    def setUp(self):
        super(BaseTestCase, self).setUp()
        if self.skip_tests:
            self.skipTest('SKIPPING FUNCTIONAL TESTS DUE TO NO CONFIG')
        self.client = self._get_client()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()

    def assertSameCertificate(self, first, second, msg=None):
        """Fail if the two certificates are not equal.
        """
        first = re.sub(r"\s+", "", first)
        second = re.sub(r"\s+", "", second)
        self.assertEqual(first, second, msg=msg)

    def assertValidSchema(self, object, schema):
        """Fail if the object does not comply with the given schema.
        """
        self.assertTrue(is_valid_response(object, schema), 'Response is not valid with the schema')
