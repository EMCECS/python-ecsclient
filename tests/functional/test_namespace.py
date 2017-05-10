import time

from ecsclient import schemas
from ecsclient.common.exceptions import ECSClientException
from tests import functional


class TestNamespace(functional.BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestNamespace, self).__init__(*args, **kwargs)
        self.namespace_1 = "functional-tests-namespace-%s" % int(time.time())
        self.namespace_2 = self.namespace_1 + '_second'
        self.namespace_3 = self.namespace_1 + '_third'

    def setUp(self):
        super(TestNamespace, self).setUp()
        self.client.namespace.create(self.namespace_1)
        self.client.namespace.create(self.namespace_3)

    def tearDown(self):
        super(TestNamespace, self).tearDown()
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
