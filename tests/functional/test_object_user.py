import time

from ecsclient import schemas
from ecsclient.common.exceptions import ECSClientException
from tests import functional


class TestObjectUser(functional.BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestObjectUser, self).__init__(*args, **kwargs)
        self.namespace_1 = "functional-tests-namespace-%s" % int(time.time())
        self.object_user_1 = "functional-tests-objectuser-%s" % int(time.time())
        self.object_user_2 = self.object_user_1 + '_second'

    def setUp(self):
        super(TestObjectUser, self).setUp()
        self.client.namespace.create(self.namespace_1)
        self.client.object_user.create(self.object_user_1, self.namespace_1)

    def tearDown(self):
        super(TestObjectUser, self).tearDown()
        for object_user in [self.object_user_1,
                            self.object_user_2]:
            try:
                self.client.object_user.delete(object_user)
            except ECSClientException:
                pass

        self.client.namespace.delete(self.namespace_1)

    def test_object_user_list(self):
        response = self.client.object_user.list()
        self.assertValidSchema(response, schemas.OBJECT_USERS)

    def test_object_user_list_with_namespace(self):
        response = self.client.object_user.list(namespace=self.namespace_1)
        self.assertValidSchema(response, schemas.OBJECT_USERS)

    def test_object_user_get(self):
        response = self.client.object_user.get(self.object_user_1)
        self.assertValidSchema(response, schemas.OBJECT_USER)

    def test_object_user_get_with_namespace(self):
        response = self.client.object_user.get(self.object_user_1, namespace=self.namespace_1)
        self.assertValidSchema(response, schemas.OBJECT_USER)

    def test_object_user_create(self):
        response = self.client.object_user.create(self.object_user_2, self.namespace_1)
        self.assertValidSchema(response, {"type": "object", "properties": {"link": schemas.LINK}, "required": ["link"]})

    def test_object_user_delete(self):
        self.client.object_user.delete(self.object_user_1, namespace=self.namespace_1)
        f = self.client.object_user.get
        self.assertRaises(ECSClientException, f, self.object_user_1, namespace=self.namespace_1)

    def test_object_user_lock_unlock(self):
        r = self.client.object_user.get_lock(self.object_user_1, namespace=self.namespace_1)
        self.assertEqual(r['isLocked'], False)

        self.client.object_user.lock(self.object_user_1, namespace=self.namespace_1)

        r = self.client.object_user.get_lock(self.object_user_1, namespace=self.namespace_1)
        self.assertEqual(r['isLocked'], True)

        self.client.object_user.unlock(self.object_user_1, namespace=self.namespace_1)

        r = self.client.object_user.get_lock(self.object_user_1, namespace=self.namespace_1)
        self.assertEqual(r['isLocked'], False)
