# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class Bucket(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def create_bucket(self, bucket_name, vpool='', filesystem_enabled=False,
                      head_type=None, namespace=None, is_stale_allowed=False,
                      metadata=None):
        """
        Creates a bucket which could be used by users to create objects.
        The bucket is created in a storage pool associated with the specified
        replication group.

        - Current user will become the bucket owner.
        - If namespace to this bucket creation does not exist, user's namespace
          is used
        - For non SYSTEM_ADMIN user, Namespace should be current user's
          namespace
        - Optional searchable metadata should be an array of JSON dictionaries,
          e.g. [{"name" : "x-amz-meta-custom", "type" : "User", "datatype" : "string"}, ...] 


        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'remote': None,
            u'name': u'bucket-test1',
            u'tags': [],
            u'global': None,
            u'vdc': None,
            u'inactive': False,
            u'id': u'namespace1.bucket-test1'
        }

        :param bucket_name: The bucket name
        :param vpool:
        :param filesystem_enabled:
        :param head_type:
        :param namespace: The namespace
        :param is_stale_allowed:
        :param search_metadata: Searchable metadata
        """
        payload = {
            "name": bucket_name,
            "vpool": vpool,
            "filesystem_enabled": filesystem_enabled,
            "head_type": head_type,
            "namespace": namespace,
            "is_stale_allowed": is_stale_allowed
            "search_metadata": metadata
        }

        log.info("Creating bucket '{0}': {1}".format(bucket_name, payload))

        if head_type:
            payload['head_type'] = head_type
        if metadata:
            payload['search_metadata'] = metadata

        return self.conn.post(url='object/bucket', json_payload=payload)

    def deactivate_bucket(self, bucket_name, namespace=None):
        """
        Deletes the specified bucket.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param bucket_name: The bucket name
        :param namespace: The namespace
        """
        msg = "Deleting bucket '{0}'".format(bucket_name)
        url = 'object/bucket/{0}/deactivate'.format(bucket_name)

        if namespace:
            url += '?namespace={0}'.format(namespace)
            msg += " in namespace '{0}'".format(namespace)

        log.info(msg)
        return self.conn.post(url=url)

    def get_buckets(self, namespace, marker='', limit=100):
        """
        Gets the list of buckets for the specified namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'MaxBuckets': 100,
            u'NextMarker': u'blah-06860733-a0a8-45b5-b4ac-b18ee1e4257d',
            u'object_bucket': [
                {
                    u'remote': None,
                    u'name': u'my-test',
                    u'tags': [
                    ],
                    u'fs_access_enabled': False,
                    u'global': None,
                    u'namespace': u'namespace1',
                    u'api_type': u'S3',
                    u'created': u'2015-06-15T18: 39: 11.957Z',
                    u'vdc': None,
                    u'default_retention': -2,
                    u'is_stale_allowed': False,
                    u'owner': u'user1',
                    u'locked': False,
                    u'notification_size': -1,
                    u'block_size': -1,
                    u'vpool': u'urn: storageos: ReplicationGroupInfo:
                                3ba1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global'
                },
                {
                    u'remote': None,
                    u'name': u'large-uploads',
                    u'tags': [
                    ],
                    u'fs_access_enabled': False,
                    u'global': None,
                    u'namespace': u'namespace1',
                    u'api_type': u'S3',
                    u'created': u'2015-06-12T17: 35: 53.366Z',
                    u'vdc': None,
                    u'default_retention': -2,
                    u'is_stale_allowed': False,
                    u'owner': u'fancyuser1',
                    u'locked': False,
                    u'notification_size': -1,
                    u'block_size': -1,
                    u'vpool': u'urn: storageos: ReplicationGroupInfo:
                                3ba1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global'
                }
            ]
        }

        List of buckets associated with the namespace

        :param namespace: The namespace to query for buckets
        :param marker: Reference to last object returned
        :param limit: Number of objects requested in current fetch
        """
        log.info("Getting all buckets in namespace '{0}'".format(namespace))

        return self.conn.get(
            url='object/bucket?namespace={0}&marker={1}&limit={2}'.format(
                namespace, marker, limit))

    def set_bucket_retention(self, bucket_name, namespace, period=2592000):
        """
        Updates the default retention setting for the specified bucket.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param bucket_name: The bucket name
        :param namespace: The namespace
        :param period: Default retention period for bucket in seconds. Defaults
        to 30 days (2592000 seconds)
        """
        payload = {
            "period": period,
            "namespace": namespace
        }

        log.info("Setting retention for bucket '{0}' in namespace "
                 "'{1}': {2}".format(bucket_name, namespace, payload))

        return self.conn.put(
            url='object/bucket/{0}/retention'.format(bucket_name),
            json_payload=payload
        )

    def get_bucket_retention(self, bucket_name, namespace=None):
        """
        Gets the retention setting for the specified bucket.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {u'period': 2592000}

        :param bucket_name: Bucket name for which the retention setting will be
        retrieved
        :param namespace: Namespace associated. If it is null, then current
        user's Namespace is used.
        """
        msg = "Getting retention for bucket '{0}'".format(bucket_name)
        url = 'object/bucket/{0}/retention'.format(bucket_name)

        if namespace:
            url += '?namespace={0}'.format(namespace)
            msg += " in namespace '{0}'".format(namespace)

        log.info(msg)
        return self.conn.get(url=url)

    def get_bucket_info(self, bucket_name, namespace=None):
        """
        Gets bucket information for the specified bucket.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'remote': None,
            u'name': u'bucket-test1',
            u'tags': [
            ],
            u'fs_access_enabled': False,
            u'global': None,
            u'namespace': u'namespace1',
            u'api_type': u'S3',
            u'created': u'2015-06-15T21: 26: 52.781Z',
            u'vdc': None,
            u'default_retention': 2592000,
            u'is_stale_allowed': False,
            u'owner': u'admin@internal',
            u'locked': False,
            u'notification_size': -1,
            u'block_size': -1,
            u'vpool': u'urn: storageos: ReplicationGroupInfo:
                        3af1fa7e-a7d1-4a9e-b8cc-e5a2c27f308d: global'
        }

        :param bucket_name: Bucket name for which information will be retrieved
        :param namespace: Namespace associated. If it is null, then current
        user's Namespace is used.
        """
        msg = "Getting info for bucket '{0}'".format(bucket_name)
        url = 'object/bucket/{0}/info'.format(bucket_name)

        if namespace:
            url += '?namespace={0}'.format(namespace)
            msg += " in namespace '{0}'".format(namespace)

        log.info(msg)
        return self.conn.get(url=url)

    def update_bucket_owner(self, bucket_name, new_owner, namespace=None):
        """
        Updates the owner for the specified bucket.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param namespace: The namespace
        :param new_owner: New owner must be a valid user
        :param bucket_name: Name of the bucket for which owner will be updated
        """
        payload = {
            "new_owner": new_owner
        }

        if namespace:
            payload['namespace'] = namespace

        log.info("Updating owner for bucket '{0}': {1}".format(bucket_name,
                                                               payload))
        return self.conn.post(
            url='object/bucket/{0}/owner'.format(bucket_name),
            json_payload=payload
        )

    def update_bucket_is_stale_allowed(self, bucket_name, is_stale_allowed,
                                       namespace=None):
        """
        Updates isStaleAllowed details for the specified bucket. If namespace
        does not exist in the request payload, the current user's namespace
        is used.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param namespace: The namespace
        :param is_stale_allowed: true/false
        :param bucket_name: Name of the bucket for which isStaleAllowed is to
        be updated
        """
        payload = {
            "is_stale_allowed": is_stale_allowed
        }

        if namespace:
            payload['namespace'] = namespace

        log.info("Updating 'isStaleAllowed' for bucket '{0}': {1}".format(
                  bucket_name, payload))

        return self.conn.post(
            url='object/bucket/{0}/isstaleallowed'.format(bucket_name),
            json_payload=payload
        )

    def get_bucket_lock(self, bucket_name, namespace=None):
        """
        Gets lock information for the specified bucket. The current user's
        namespace is used.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'isLocked': False,
            u'bucket_name': u'bucket-test1'
        }

        :param bucket_name: Example: The bucket name to get lock information
        :param namespace: Name of the bucket for which lock information is to
        be retrieved
        """
        msg = "Getting lock info for bucket '{0}'".format(bucket_name)
        url = 'object/bucket/{0}/lock'.format(bucket_name)

        if namespace:
            url += '?namespace={0}'.format(namespace)
            msg += " in namespace '{0}'".format(namespace)

        log.info(msg)
        return self.conn.get(url=url)

    def set_lock_bucket(self, bucket_name, is_locked='false', namespace=None):
        """
        Locks or unlocks the specified bucket. Current user's namespace
        is used.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param bucket_name: Name of the bucket which is to be locked/unlocked.
        :param is_locked: Set to "true" for lock bucket and "false" for unlock
        bucket.
        :param namespace: The namespace
        """
        payload = {}

        if namespace:
            payload['namespace'] = namespace

        log.info("Setting lock to '{0}' for bucket '{1}': {2}".format(
                  is_locked, bucket_name, payload))

        return self.conn.put(
            url='object/bucket/{0}/lock/{1}'.format(bucket_name, is_locked),
            json_payload=payload
        )

    def update_bucket_quota(self, bucket_name, block_size, notification_size,
                            namespace=None):
        """
        Updates the quota for the specified bucket.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param bucket_name: Name of the bucket for which the quota is to be
        updated
        :param block_size:
        :param notification_size:
        :param namespace: The namespace
        """
        payload = {
            "blockSize": block_size,
            "notificationSize": notification_size
        }

        if namespace:
            payload['namespace'] = namespace

        log.info("Updating quota for bucket '{0}': {1}".format(bucket_name,
                                                               payload))
        return self.conn.put(
            url='object/bucket/{0}/quota'.format(bucket_name),
            json_payload=payload
        )

    def get_bucket_quota(self, bucket_name, namespace=None):
        """
        Gets the quota for the given bucket and namespace. The namespace with
        which the bucket is associated can be specified as a query parameter.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'blockSize': 1,
            u'notificationSize': 2,
            u'namespace': u'namespace1',
            u'bucketname': u'bucket-test1'
        }

        :param bucket_name: Name of the bucket which for which quota is to be
        retrieved
        :param namespace: Namespace with which bucket is associated. If it is
        null, the current user's namespace is used.
        """
        msg = "Getting quota for bucket '{0}'".format(bucket_name)
        url = 'object/bucket/{0}/quota'.format(bucket_name)

        if namespace:
            url += '?namespace={0}'.format(namespace)
            msg += " in namespace '{0}'".format(namespace)

        log.info(msg)
        return self.conn.get(url=url)

    def delete_bucket_quota(self, bucket_name, namespace=None):
        """
        Deletes the quota setting for the given bucket and namespace.
        The namespace with which the bucket is associated can be specified as
        a query parameter.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param bucket_name: Name of the bucket for which the quota is to
        be deleted
        :param namespace: Namespace with which bucket is associated. If it is
        null, the current user's namespace is used.
        """
        params = None

        if namespace:
            params = {'namespace': namespace}

        log.info("Deleting quota for bucket '{0}'".format(bucket_name))

        return self.conn.delete(
            url='object/bucket/{0}/quota'.format(bucket_name),
            params=params
        )

    def get_bucket_acl(self, bucket_name, namespace=None):
        """
        Gets the ACL for the given bucket. Current user's namespace is used.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'namespace': u'namespace1',
            u'bucket': u'bucket-test1',
            u'permission': []
        }

        :param bucket_name: Name of the bucket for which ACL is to be updated.
        :param namespace: Namespace with which bucket is associated. If it is
        null, the current user's namespace is used.
        """
        params = None

        if namespace:
            params = {'namespace': namespace}

        log.info("Getting ACL for bucket '{0}'".format(bucket_name))

        return self.conn.get(
            url='object/bucket/{0}/acl'.format(bucket_name),
            params=params
        )

    def get_acl_permissions(self):
        """
        Gets all ACL permissions.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'permission': [
                {
                    u'display_name': u'read',
                    u'id': u'read'
                },
                {
                    u'display_name': u'readACL',
                    u'id': u'read_acl'
                },
                {
                    u'display_name': u'write',
                    u'id': u'write'
                },
                {
                    u'display_name': u'writeACL',
                    u'id': u'write_acl'
                },
                {
                    u'display_name': u'execute',
                    u'id': u'execute'
                },
                {
                    u'display_name': u'fullcontrol',
                    u'id': u'full_control'
                },
                {
                    u'display_name': u'privilegedwrite',
                    u'id': u'privileged_write'
                },
                {
                    u'display_name': u'delete',
                    u'id': u'delete'
                },
                {
                    u'display_name': u'none',
                    u'id': u'none'
                }
            ]
        }
        """
        log.info('Getting all ACLs')
        return self.conn.get(url='object/bucket/acl/permissions')

    def get_acl_groups(self):
        """
        Gets all ACL groups.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'group': [
                {
                    u'display_name': u'public',
                    u'id': u'public',
                    u'description': u'allusersincludingauthenticatedusers&anon'
                },
                {
                    u'display_name': u'allusers',
                    u'id': u'all_users',
                    u'description': u'allauthenticatedusers'
                },
                {
                    u'display_name': u'logdelivery',
                    u'id': u'log_delivery',
                    u'description': u'specifictoS3'
                },
                {
                    u'display_name': u'other',
                    u'id': u'other',
                    u'description': u'allauthenticatedusersbuttheowner'
                }
            ]
        }
        """
        log.info('Getting all ACL groups')
        return self.conn.get(url='object/bucket/acl/groups')
