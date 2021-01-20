import os
from ecsclient import schemas
from ecsclient.common.exceptions import ECSClientException
from tests import functional
from six.moves import configparser


class TestTenant(functional.BaseTestCase):
    """
    Test conf sample
    [func_test]
    token_endpoint = https://10.0.1.1:4443/login
    ecs_endpoint = https://10.0.1.1:4443
    username = root
    password = k912oz2chpsy8tny
    api_version = 3
    license_file = /home/user/license.lic
    override_header = true
    account_id = 6bd95656-42df-4e9e-9b19-b05a660eca81
    """
    def __init__(self, *args, **kwargs):
        super(TestTenant, self).__init__(*args, **kwargs)
        config_file = os.environ.get('ECS_TEST_CONFIG_FILE',
                                     os.path.join(os.getcwd(), "tests/test.conf"))
        config = configparser.ConfigParser()
        config.read(config_file)
        self.config = config
        if config.has_section('func_test'):
            self.tenant = config.get('func_test', 'account_id')
        else:
            self.skip_tests = True

    def setUp(self):
        super(TestTenant, self).setUp()
        self.create_account()
        if self.skip_tests:
            self.skipTest('SKIPPING FUNCTIONAL TESTS DUE TO NO CONFIG')
        self.client.tenant.create(self.tenant)

    def tearDown(self):
        super(TestTenant, self).tearDown()
        try:
            self.client.tenant.delete(self.tenant)
        except ECSClientException:
            pass

    def test_tenants_list(self):
        response = self.client.tenant.list()
        self.assertValidSchema(response, schemas.TENANTS)

    def test_tenants_get_one(self):
        response = self.client.tenant.get(self.tenant)
        self.assertValidSchema(response, schemas.TENANT)

    def test_tenants_delete(self):
        self.client.tenant.delete(self.tenant)
        f = self.client.tenant.get
        self.assertRaises(ECSClientException, f, self.tenant)
