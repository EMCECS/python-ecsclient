import time

from ecsclient import schemas
from ecsclient.common.exceptions import ECSClientException
from tests import functional


class TestPasswordGroup(functional.BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestPasswordGroup, self).__init__(*args, **kwargs)
        self.namespace_1 = "functional-tests-namespace-%s" % int(time.time())
        self.object_user_1 = "functional-tests-objectuser-%s" % int(time.time())
        self.object_user_2 = self.object_user_1 + '_second'
        self.password_1 = "fake-password-123"
        self.password_2 = "fake-password-456"
        self.groups_list_1 = ['admin']
        self.groups_list_2 = ['admin', 'user']

    def setUp(self):
        super(TestPasswordGroup, self).setUp()
        self.client.namespace.create(self.namespace_1)
        self.client.object_user.create(self.object_user_1, self.namespace_1)
        self.client.password_group.create(self.object_user_1,
                                          self.password_1,
                                          self.groups_list_1,
                                          namespace=self.namespace_1)

    def tearDown(self):
        super(TestPasswordGroup, self).tearDown()
        for object_user in [self.object_user_1,
                            self.object_user_2]:
            try:
                self.client.object_user.delete(object_user)
            except ECSClientException:
                pass
        self.client.namespace.delete(self.namespace_1)

    def test_password_group_create_for_user(self):
        self.client.password_group.create(user_id=self.object_user_2,
                                          namespace=self.namespace_1,
                                          password=self.password_2,
                                          groups_list=self.groups_list_2)

        response = self.client.password_group.get(user_id=self.object_user_2,
                                                  namespace=self.namespace_1)

        self.assertValidSchema(response, schemas.GROUP_LIST)
        self.assertEqual(response['groups_list'], self.groups_list_2)

    def test_password_group_get_by_user(self):
        response = self.client.password_group.get(user_id=self.object_user_1,
                                                  namespace=self.namespace_1)

        self.assertValidSchema(response, schemas.GROUP_LIST)
        self.assertEqual(response['groups_list'], self.groups_list_1)

    def test_password_group_update_for_user(self):
        self.assertNotEqual(self.groups_list_1, self.groups_list_2)

        response = self.client.password_group.get(user_id=self.object_user_1,
                                                  namespace=self.namespace_1)
        self.assertEqual(response['groups_list'], self.groups_list_1)

        self.client.password_group.update(user_id=self.object_user_1,
                                          namespace=self.namespace_1,
                                          password=self.password_2,
                                          groups_list=self.groups_list_2)

        response = self.client.password_group.get(user_id=self.object_user_1,
                                                  namespace=self.namespace_1)
        self.assertEqual(response['groups_list'], self.groups_list_2)

    def test_password_group_delete_for_user(self):
        self.client.password_group.delete(user_id=self.object_user_1,
                                          namespace=self.namespace_1)
        f = self.client.password_group.get
        self.assertRaises(ECSClientException, f, self.object_user_1)
