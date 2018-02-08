import time

from ecsclient import schemas
from ecsclient.common.exceptions import ECSClientException
from tests import functional


class TestSecretKey(functional.BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestSecretKey, self).__init__(*args, **kwargs)
        self.namespace_1 = "functional-tests-namespace-%s" % int(time.time())
        self.object_user_1 = "functional-tests-objectuser-%s" % int(time.time())
        self.object_user_current = None
        self.secret_key_1 = "E3GooHbvQXSxHplji1aPEGZilIEWYfveJQtFIrAF"
        self.current_user_created = False

    def setUp(self):
        super(TestSecretKey, self).setUp()
        self.client.namespace.create(self.namespace_1)
        self.client.object_user.create(self.object_user_1, self.namespace_1)
        self.client.secret_key.create(user_id=self.object_user_1,
                                      namespace=self.namespace_1,
                                      secret_key=self.secret_key_1)
        r = self.client.user_info.whoami()
        self.object_user_current = r['common_name']
        try:
            self.client.object_user.create(self.object_user_current, self.namespace_1)
            self.current_user_created = True
        except ECSClientException:
            pass
        self.client.secret_key.create()

    def tearDown(self):
        super(TestSecretKey, self).tearDown()
        self.client.object_user.delete(self.object_user_1)
        if self.current_user_created:
            self.client.object_user.delete(self.object_user_current)
        self.client.namespace.delete(self.namespace_1)

    def test_secret_key_get_authenticated_user(self):
        response = self.client.secret_key.get()
        self.assertValidSchema(response, schemas.SECRET_KEYS)

    def test_secret_key_get_by_user(self):
        response = self.client.secret_key.get(user_id=self.object_user_1,
                                              namespace=self.namespace_1)
        self.assertValidSchema(response, schemas.SECRET_KEYS)
        self.assertEqual(response['secret_key_1'], self.secret_key_1)

    def test_secret_key_create_authenticated_user(self):
        response = self.client.secret_key.create()
        self.assertValidSchema(response, schemas.SECRET_KEY)

    def test_secret_key_create_for_user(self):
        secret_key = 'zDR3nIO9ywbdpabxKSbnB3NKGIclBSEpyCkh0KJB'
        response = self.client.secret_key.create(user_id=self.object_user_1,
                                                 namespace=self.namespace_1,
                                                 expiry_time=60,
                                                 secret_key=secret_key)
        self.assertValidSchema(response, schemas.SECRET_KEY)
        self.assertEqual(response['secret_key'], secret_key)

    def test_secret_key_delete_authenticated_user(self):
        response = self.client.secret_key.get()
        self.assertNotEqual(response['secret_key_1'] or response['secret_key_2'], "")

        self.client.secret_key.delete()

        response = self.client.secret_key.get()
        self.assertEqual(response['secret_key_1'], "")
        self.assertEqual(response['secret_key_2'], "")

    def test_secret_key_delete_for_user(self):
        response = self.client.secret_key.get(user_id=self.object_user_1, namespace=self.namespace_1)
        self.assertNotEqual(response['secret_key_1'] or response['secret_key_2'], "")

        self.client.secret_key.delete(user_id=self.object_user_1, namespace=self.namespace_1)

        response = self.client.secret_key.get(user_id=self.object_user_1, namespace=self.namespace_1)
        self.assertEqual(response['secret_key_1'], "")
        self.assertEqual(response['secret_key_2'], "")

    def test_secret_key_replace(self):
        secret_key = 'A3GooHbvQXSxHplji1aPEGZilIEWYfveJQtFIrAF'

        self.client.secret_key.delete(user_id=self.object_user_1, namespace=self.namespace_1)

        response = self.client.secret_key.get(user_id=self.object_user_1, namespace=self.namespace_1)
        self.assertEqual(response['secret_key_1'], "")
        self.assertEqual(response['secret_key_2'], "")

        self.client.secret_key.create(user_id=self.object_user_1,
                                      namespace=self.namespace_1,
                                      secret_key=secret_key)

        response = self.client.secret_key.get(user_id=self.object_user_1, namespace=self.namespace_1)
        self.assertEqual(response['secret_key_1'], secret_key)
        self.assertEqual(response['secret_key_2'], "")
