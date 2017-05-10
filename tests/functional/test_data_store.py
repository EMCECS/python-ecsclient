import time

from ecsclient import schemas
from tests import functional


class TestDataStore(functional.BaseTestCase):
    def setUp(self):
        super(TestDataStore, self).setUp()

        # Get a data store ID
        r = self.client.data_store.list()
        self.data_store_1_id = r['data_store'][0]['id']

        # Get a storage pool ID
        r = self.client.data_store.get(self.data_store_1_id)
        self.storage_pool_1_id = r['varray']

        # Create a new data store to get a task ID
        self.data_store_2_name = "functional-tests-datastore-%s" % int(time.time())
        r = self.client.data_store.create(name=self.data_store_2_name,
                                          description="Data Store for functional test",
                                          node_id=self.data_store_1_id,
                                          storage_pool_id=self.storage_pool_1_id)
        self.task_1_id = r['task'][0]['op_id']

    def test_data_store_list(self):
        response = self.client.data_store.list()
        self.assertValidSchema(response, schemas.DATA_STORES)

    def test_data_store_get(self):
        response = self.client.data_store.get(self.data_store_1_id)
        self.assertValidSchema(response, schemas.DATA_STORE)
        self.assertEqual(response['varray'], self.storage_pool_1_id)

    def test_data_store_get_by_storage_pool(self):
        response = self.client.data_store.get_by_storage_pool(self.storage_pool_1_id)
        self.assertValidSchema(response, schemas.DATA_STORES_COMMODITY)
        self.assertEqual(response['commodity_data_store'][0]['varray'], self.storage_pool_1_id)

    def test_data_store_create(self):
        response = self.client.data_store.create(name=self.data_store_2_name,
                                                 description="Data Store for functional test",
                                                 node_id=self.data_store_1_id,
                                                 storage_pool_id=self.storage_pool_1_id)
        self.assertValidSchema(response, schemas.DATA_STORE_TASKS)

    def test_data_store_delete(self):
        # TODO: API is returning an error. Need to investigate
        self.skipTest('Skipping until investigated')
        # Try to delete a non-existent data store
        response = self.client.data_store.delete(data_store_id='9.9.9.9')
        self.assertValidSchema(response, schemas.DATA_STORE_TASKS)

    def test_data_store_get_task(self):
        response = self.client.data_store.get_task(data_store_id=self.data_store_1_id, op_id=self.task_1_id)
        self.assertValidSchema(response, schemas.DATA_STORE_TASK)
        self.assertEqual(response['op_id'], self.task_1_id)
