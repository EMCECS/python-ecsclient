import time

from ecsclient import schemas
from ecsclient.common.exceptions import ECSClientException
from tests import functional


class TestStoragePool(functional.BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestStoragePool, self).__init__(*args, **kwargs)
        self.storage_pool_1 = "functional-tests-storagepool-%s" % int(time.time())
        self.storage_pool_2 = self.storage_pool_1 + '_second'
        self.storage_pool_3 = self.storage_pool_1 + '_third'

    def setUp(self):
        super(TestStoragePool, self).setUp()
        r = self.client.storage_pool.create(self.storage_pool_1)
        self.storage_pool_1_id = r['id']
        self.storage_pool_2_id = 'placeholder'
        r = self.client.storage_pool.create(self.storage_pool_3)
        self.storage_pool_3_id = r['id']

    def tearDown(self):
        super(TestStoragePool, self).tearDown()
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
