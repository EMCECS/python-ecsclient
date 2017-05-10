import time

from ecsclient import schemas
from ecsclient.common.exceptions import ECSClientException
from tests import functional


class TestReplicationGroup(functional.BaseTestCase):

    def setUp(self):
        super(TestReplicationGroup, self).setUp()
        # Initialize the resource names
        self.storage_pool_1 = "functional-tests-storagepool-%s" % int(time.time())
        self.replication_group_1 = "functional-tests-replicationgroup-%s" % int(time.time())
        self.replication_group_1_id = "placeholder"
        self.replication_group_2 = self.replication_group_1 + '_second'
        self.replication_group_2_id = "placeholder"

        # Get the local VDC
        r = self.client.vdc.get_local()
        self.vdc_1_id = r['id']

        # Create a Storage Pool
        r = self.client.storage_pool.create(self.storage_pool_1)
        self.storage_pool_1_id = r['id']

        # Create a Replication Group
        zone_mappings = [(
            self.vdc_1_id,
            self.storage_pool_1_id
        )]
        r = self.client.replication_group.create(self.replication_group_1, zone_mappings)
        self.replication_group_1_id = r['id']

    def tearDown(self):
        super(TestReplicationGroup, self).tearDown()

        try:
            self.client.storage_pool.delete(self.storage_pool_1_id)
        except ECSClientException:
            pass

        for replication_group_id in [self.replication_group_1_id,
                                     self.replication_group_2_id]:
            try:
                self.client.replication_group.delete(replication_group_id)
            except ECSClientException:
                pass

    def test_replication_group_list(self):
        response = self.client.replication_group.list()
        self.assertValidSchema(response, schemas.REPLICATION_GROUPS)

    def test_replication_group_get_one(self):
        response = self.client.replication_group.get(self.replication_group_1_id)
        self.assertValidSchema(response, schemas.REPLICATION_GROUP)
        self.assertEqual(response['id'], self.replication_group_1_id)

    def test_replication_group_update(self):
        new_name = self.replication_group_1 + '_updated'
        response = self.client.replication_group.get(self.replication_group_1_id)
        self.assertNotEqual(response['name'], new_name)
        self.assertNotEqual(response['description'], new_name + ' description')
        self.assertTrue(response['isAllowAllNamespaces'])
        self.assertFalse(response['enable_rebalancing'])

        self.client.replication_group.update(self.replication_group_1_id,
                                             name=new_name,
                                             description=new_name + ' description',
                                             allow_all_namespaces=False,
                                             enable_rebalancing=True)

        response = self.client.replication_group.get(self.replication_group_1_id)
        self.assertEqual(response['name'], new_name)
        self.assertEqual(response['description'], new_name + ' description')
        self.assertFalse(response['isAllowAllNamespaces'])
        self.assertTrue(response['enable_rebalancing'])

    def test_replication_group_create(self):
        zone_mappings = [(
            self.vdc_1_id,
            self.storage_pool_1_id
        )]
        response = self.client.replication_group.create(self.replication_group_2,
                                                        zone_mappings,
                                                        description=self.replication_group_2 + " description",
                                                        allow_all_namespaces=False,
                                                        is_full_rep=False,
                                                        enable_rebalancing=True)
        self.assertValidSchema(response, schemas.REPLICATION_GROUP)
        self.assertEqual(response['name'], self.replication_group_2)
        self.assertEqual(response['description'], self.replication_group_2 + " description")
        self.assertFalse(response['isAllowAllNamespaces'])
        self.assertFalse(response['isFullRep'])
        self.assertTrue(response['enable_rebalancing'])
        self.assertEqual(response['varrayMappings'][0]['name'], self.vdc_1_id)
        self.assertEqual(response['varrayMappings'][0]['value'], self.storage_pool_1_id)

    def test_replication_group_delete(self):
        self.client.replication_group.delete(self.replication_group_1_id)
        f = self.client.replication_group.get
        self.assertRaises(ECSClientException, f, self.replication_group_1_id)
