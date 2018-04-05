import time

from ecsclient import schemas
from ecsclient.common.exceptions import ECSClientException
from tests import functional


class TestBucket(functional.BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestBucket, self).__init__(*args, **kwargs)
        self.bucket_1 = "functional-tests-bucket-%s" % int(time.time())
        self.bucket_2 = self.bucket_1 + '_second'
        self.namespace_1 = "functional-tests-namespace-%s" % int(time.time())
        self.replication_group_1 = "functional-tests-replicationgroup-%s" % int(time.time())
        self.replication_group_1_id = "placeholder"
        self.storage_pool_1 = "functional-tests-storagepool-%s" % int(time.time())
        self.object_user = None
        self.object_user_created = False
        self.replication_group_created = False

    def setUp(self):
        super(TestBucket, self).setUp()
        # Create a namespace
        self.client.namespace.create(self.namespace_1)
        # Create an object user with the current logged in user name
        r = self.client.user_info.whoami()
        self.object_user = r['common_name']
        try:
            self.client.object_user.create(self.object_user, self.namespace_1)
            self.object_user_created = True
        except ECSClientException:
            pass
        # Create a Replication Group
        r = self.client.replication_group.list()
        if len(r['data_service_vpool']) > 0:
            self.replication_group_created = False
            self.replication_group_1_id = r['data_service_vpool'][0]['id']
        else:
            r = self.client.vdc.get_local()
            self.vdc_1_id = r['id']
            r = self.client.storage_pool.create(self.storage_pool_1)
            self.storage_pool_1_id = r['id']
            zone_mappings = [(
                self.vdc_1_id,
                self.storage_pool_1_id
            )]
            r = self.client.replication_group.create(self.replication_group_1, zone_mappings)
            self.replication_group_created = True
            self.replication_group_1_id = r['id']

        self.client.bucket.create(self.bucket_1,
                                  namespace=self.namespace_1,
                                  replication_group=self.replication_group_1_id)

    def tearDown(self):
        super(TestBucket, self).tearDown()
        for bucket in [self.bucket_1,
                       self.bucket_2]:
            try:
                self.client.bucket.delete(bucket, namespace=self.namespace_1)
            except ECSClientException:
                pass

        if self.object_user_created:
            self.client.object_user.delete(self.object_user)
        self.client.namespace.delete(self.namespace_1)
        if self.replication_group_created:
            self.client.storage_pool.delete(self.storage_pool_1_id)
            self.client.replication_group.delete(self.replication_group_1_id)

    def test_bucket_list(self):
        response = self.client.bucket.list(self.namespace_1)
        self.assertValidSchema(response, schemas.BUCKET_LIST)

    def test_bucket_create(self):
        response = self.client.bucket.create(self.bucket_2,
                                             namespace=self.namespace_1,
                                             replication_group=self.replication_group_1_id,
                                             filesystem_enabled=False,
                                             head_type='s3',
                                             stale_allowed=True,
                                             encryption_enabled=False
                                             )
        self.assertValidSchema(response, schemas.BUCKET_SHORT)
        self.assertEqual(response['name'], self.bucket_2)

    def test_bucket_get(self):
        response = self.client.bucket.get(self.bucket_1, namespace=self.namespace_1)
        self.assertValidSchema(response, schemas.BUCKET)
        self.assertEqual(response['name'], self.bucket_1)

    def test_bucket_set_owner(self):
        self.client.bucket.set_owner(self.bucket_1,
                                     self.object_user,
                                     namespace=self.namespace_1)

        response = self.client.bucket.get(self.bucket_1, namespace=self.namespace_1)
        self.assertEqual(response['owner'], self.object_user)

    def test_bucket_set_stale_allowed(self):
        response = self.client.bucket.get(self.bucket_1, namespace=self.namespace_1)
        self.assertEqual(response['is_stale_allowed'], False)

        self.client.bucket.set_stale_allowed(self.bucket_1, True, namespace=self.namespace_1)

        response = self.client.bucket.get(self.bucket_1, namespace=self.namespace_1)
        self.assertEqual(response['is_stale_allowed'], True)

    def test_bucket_lock(self):
        self.client.bucket.set_lock(self.bucket_1, is_locked=True, namespace=self.namespace_1)
        response = self.client.bucket.get_lock(self.bucket_1, namespace=self.namespace_1)
        self.assertEqual(response['isLocked'], True)

        self.client.bucket.set_lock(self.bucket_1, is_locked=False, namespace=self.namespace_1)
        response = self.client.bucket.get_lock(self.bucket_1, namespace=self.namespace_1)
        self.assertEqual(response['isLocked'], False)

    def test_bucket_quota(self):
        self.client.bucket.set_quota(self.bucket_1, namespace=self.namespace_1,
                                     block_size=10,
                                     notification_size=1)
        response = self.client.bucket.get_quota(self.bucket_1, namespace=self.namespace_1)
        self.assertEqual(response['blockSize'], 10)
        self.assertEqual(response['notificationSize'], 1)

        self.client.bucket.delete_quota(self.bucket_1, namespace=self.namespace_1)
        response = self.client.bucket.get_quota(self.bucket_1, namespace=self.namespace_1)
        self.assertEqual(response['blockSize'], -1)
        self.assertEqual(response['notificationSize'], -1)

    def test_bucket_acl_permissions(self):
        response = self.client.bucket.get_acl_permissions()
        self.assertValidSchema(response, schemas.BUCKET_ACL_PERMISSIONS)

    def test_bucket_acl_groups(self):
        response = self.client.bucket.get_acl_groups()
        self.assertValidSchema(response, schemas.BUCKET_ACL_GROUPS)

    def test_bucket_acl(self):
        user_acl = [{'permission': ['full_control'], 'user': self.object_user}]
        group_acl = [{'permission': ['read'], 'group': 'public'}]
        customgroup_acl = [{'permission': ['delete', 'read', 'write'], 'customgroup': 'cgroup1'}]

        self.client.bucket.set_acl(self.bucket_1,
                                   namespace=self.namespace_1,
                                   owner=self.object_user,
                                   default_group='public',
                                   user_acl=user_acl,
                                   group_acl=group_acl,
                                   customgroup_acl=customgroup_acl)

        acl = self.client.bucket.get_acl(self.bucket_1,
                                         namespace=self.namespace_1)

        self.assertEqual(acl['acl']['owner'], self.object_user)
        self.assertEqual(acl['acl']['default_group'], 'public')
        self.assertEqual(acl['acl']['group_acl'], group_acl)
        self.assertEqual(acl['acl']['user_acl'], user_acl)
        acl['acl']['customgroup_acl'][0]['permission'].sort()
        self.assertEqual(acl['acl']['customgroup_acl'], customgroup_acl)
        self.assertEqual(acl['bucket'], self.bucket_1)
        self.assertEqual(acl['namespace'], self.namespace_1)

        # Clear ACLs

        self.client.bucket.set_acl(self.bucket_1,
                                   namespace=self.namespace_1)
        acl = self.client.bucket.get_acl(self.bucket_1,
                                         namespace=self.namespace_1)

        self.assertEqual(acl['acl']['group_acl'], [])
        self.assertEqual(acl['acl']['user_acl'], [])
        self.assertEqual(acl['acl']['customgroup_acl'], [])
        self.assertEqual(acl['bucket'], self.bucket_1)
        self.assertEqual(acl['namespace'], self.namespace_1)

    def test_bucket_user_metadata(self):
        self.client.bucket.set_metadata(self.bucket_1,
                                        "key1",
                                        "value1",
                                        "S3",
                                        namespace=self.namespace_1)

        response = self.client.bucket.get_metadata(self.bucket_1, "S3", namespace=self.namespace_1)
        self.assertValidSchema(response, schemas.BUCKET_USER_METADATA)
        self.assertEqual(response['metadata'][0]['name'], "key1")
        self.assertEqual(response['metadata'][0]['value'], "value1")
        self.assertEqual(response['head_type'], "S3")

        self.client.bucket.delete_metadata(self.bucket_1, "S3", namespace=self.namespace_1)
        f = self.client.bucket.get_metadata
        self.assertRaises(ECSClientException, f, self.bucket_1, "S3", namespace=self.namespace_1)

    def test_bucket_system_metadata(self):
        response = self.client.bucket.get_system_metadata_keys()
        self.assertValidSchema(response, schemas.BUCKET_SYSTEM_METADATA)
