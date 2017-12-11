from ecsclient import schemas
from tests import functional


class TestCapacity(functional.BaseTestCase):

    def test_get_cluster_capacity(self):
        response = self.client.capacity.get_cluster_capacity()
        self.assertValidSchema(response, schemas.CAPACITY)

    def test_get_cluster_capacity_storage_pool(self):
        sps = self.client.storage_pool.list()
        response = self.client.capacity.get_cluster_capacity(storage_pool_id=sps['varray'][0]['id'])
        self.assertValidSchema(response, schemas.CAPACITY)
