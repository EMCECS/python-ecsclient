import time

from ecsclient import schemas
from ecsclient.common.exceptions import ECSClientException
from tests import functional


class TestManagementUser(functional.BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestManagementUser, self).__init__(*args, **kwargs)
        self.management_user_1 = "functional-tests-managementuser-%s" % int(time.time())
        self.management_user_2 = self.management_user_1 + '_second'

    def setUp(self):
        super(TestManagementUser, self).setUp()
        self.client.management_user.create(self.management_user_1,
                                           password='fake-password-123')

    def tearDown(self):
        super(TestManagementUser, self).tearDown()
        for management_user in [self.management_user_1,
                                self.management_user_2]:
            try:
                self.client.management_user.delete(management_user)
            except ECSClientException:
                pass

    def test_management_user_list(self):
        response = self.client.management_user.list()
        self.assertValidSchema(response, schemas.MANAGEMENT_USERS)

    def test_management_user_get(self):
        response = self.client.management_user.get(self.management_user_1)
        self.assertValidSchema(response, schemas.MANAGEMENT_USER)
        self.assertEqual(response['userId'], self.management_user_1)

    def test_management_user_create(self):
        response = self.client.management_user.create(self.management_user_2,
                                                      password='fake-password-123',
                                                      is_system_admin=True,
                                                      is_system_monitor=True,
                                                      is_security_admin=True)
        self.assertValidSchema(response, schemas.MANAGEMENT_USER)
        self.assertEqual(response['userId'], self.management_user_2)
        self.assertTrue(response['isSystemAdmin'])
        self.assertTrue(response['isSystemMonitor'])
        self.assertTrue(response['isSecurityAdmin'])

    def test_management_user_delete(self):
        self.client.management_user.delete(self.management_user_1)
        f = self.client.management_user.get
        self.assertRaises(ECSClientException, f, self.management_user_1)

    def test_management_user_update(self):
        response = self.client.management_user.get(self.management_user_1)
        self.assertFalse(response['isSystemAdmin'])
        self.assertFalse(response['isSystemMonitor'])
        self.assertFalse(response['isSecurityAdmin'])

        self.client.management_user.update(self.management_user_1,
                                           password='fake-password-123',
                                           is_system_admin=True,
                                           is_system_monitor=True,
                                           is_security_admin=True)

        response = self.client.management_user.get(self.management_user_1)
        self.assertTrue(response['isSystemAdmin'])
        self.assertTrue(response['isSystemMonitor'])
        self.assertTrue(response['isSecurityAdmin'])
