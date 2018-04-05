import json
import logging

log = logging.getLogger(__name__)


class Bucket(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def create(self, bucket_name, replication_group='', filesystem_enabled=False,
               head_type=None, namespace=None, stale_allowed=False,
               metadata=None, encryption_enabled=False):
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
            "name": "bucket5",
            "id": "s3.bucket5",
            "inactive": false,
            "global": null,
            "remote": null,
            "vdc": null,
            "tags": [],
            "search_metadata":{
              "metadata":[
                 {
                    "type": "User",
                    "datatype":"integer",
                    "name":"x-amz-meta-custom"
                 }
              ]
            }
        }

        :param bucket_name: The bucket name
        :param replication_group: Replication group identifier
        :param filesystem_enabled: Boolean indicating whether file-system is enabled for this bucket
        :param head_type: Indicates the object head type that is allowed to access the bucket.
        If the bucket has FS-Enabled, then the FS heads are implicitly allowed to access this bucket
        :param namespace: Namespace associated with the user/tenant that is allowed to access the bucket
        :param stale_allowed: Boolean indicating whether to allow stale data in bucket
        :param metadata: Searchable tags assigned to objects created within the bucket.
        Example: [{"name" : "x-amz-meta-custom", "type" : "User", "datatype" : "string"}, ...]
        :param encryption_enabled: Boolean indicating whether is enabled for the bucket
        """
        payload = {
            "name": bucket_name,
            "vpool": replication_group,
            "filesystem_enabled": filesystem_enabled,
            "is_stale_allowed": stale_allowed,
            "is_encryption_enabled": encryption_enabled,
        }

        log.info("Creating bucket '{}'".format(bucket_name))

        if namespace:
            payload['namespace'] = namespace
        if head_type:
            payload['head_type'] = head_type
        if metadata:
            payload['search_metadata'] = metadata

        return self.conn.post('object/bucket', json_payload=payload)

    def delete(self, bucket_name, namespace=None):
        """
        Deletes the specified bucket.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param bucket_name: The bucket name to be deleted
        :param namespace: Namespace associated. If not provided, then current user's namespace is used
        """
        msg = "Deleting bucket '{}'".format(bucket_name)
        url = 'object/bucket/{}/deactivate'.format(bucket_name)

        if namespace:
            url += '?namespace={}'.format(namespace)
            msg += " in namespace '{}'".format(namespace)

        log.info(msg)
        return self.conn.post(url)

    def list(self, namespace, marker='', limit=100):
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

        :param namespace: The namespace to query for buckets
        :param marker: Reference to last object returned
        :param limit: Number of objects requested in current fetch
        """
        log.info("Getting all buckets in namespace '{}'".format(namespace))

        return self.conn.get('object/bucket?namespace={namespace}&marker={marker}&limit={limit}'.format(
            namespace=namespace,
            marker=marker,
            limit=limit))

    def set_retention(self, bucket_name, namespace, period=2592000):
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

        return self.conn.put('object/bucket/{}/retention'.format(bucket_name),
                             json_payload=payload)

    def get_retention(self, bucket_name, namespace=None):
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
        url = 'object/bucket/{}/retention'.format(bucket_name)
        msg = "Getting retention for bucket '{}'".format(bucket_name)

        if namespace:
            url += '?namespace={}'.format(namespace)
            msg += " in namespace '{}'".format(namespace)

        log.info(msg)
        return self.conn.get(url)

    def get(self, bucket_name, namespace=None):
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
        msg = "Getting info for bucket '{}'".format(bucket_name)
        url = 'object/bucket/{}/info'.format(bucket_name)

        if namespace:
            url += '?namespace={}'.format(namespace)
            msg += " in namespace '{}'".format(namespace)

        log.info(msg)
        return self.conn.get(url)

    def set_owner(self, bucket_name, new_owner, namespace=None):
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

        log.info("Updating owner for bucket '{}': {}".format(bucket_name, new_owner))
        return self.conn.post('object/bucket/{}/owner'.format(bucket_name),
                              json_payload=payload)

    def set_stale_allowed(self, bucket_name, stale_allowed, namespace=None):
        """
        Updates isStaleAllowed details for the specified bucket. If namespace
        does not exist in the request payload, the current user's namespace
        is used.

        If you set this flag ON, and a temporary site outage occurs, objects that
        you access in this bucket might have been updated at the failed site but
        changes might not have been propagated to the site from which you are
        accessing the object.Hence, you are prepared to accept that the objects
        you read might not be up to date.

        If the flag is turned OFF, data in the zone which has the temporary outage is not
        available for access from other zones and object reads for data which has its
        primary in the failed site will fail.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param bucket_name: Name of the bucket for which isStaleAllowed is to
        be updated
        :param stale_allowed: true/false
        :param namespace: Namespace associated with the user/tenant that is
        allowed to access the bucket
        """
        payload = {
            "is_stale_allowed": stale_allowed
        }

        if namespace:
            payload['namespace'] = namespace

        log.info("Updating 'isStaleAllowed' for bucket '{}': {}".format(
            bucket_name, stale_allowed))

        return self.conn.post('object/bucket/{}/isstaleallowed'.format(bucket_name),
                              json_payload=payload)

    def get_lock(self, bucket_name, namespace=None):
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
        msg = "Getting lock info for bucket '{}'".format(bucket_name)
        url = 'object/bucket/{}/lock'.format(bucket_name)

        if namespace:
            url += '?namespace={}'.format(namespace)
            msg += " in namespace '{}'".format(namespace)

        log.info(msg)
        return self.conn.get(url)

    def set_lock(self, bucket_name, is_locked=False, namespace=None):
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
        :param is_locked: Set to True to lock the bucket and False to unlock the
        bucket
        :param namespace: The namespace
        """
        payload = {}
        if namespace:
            payload['namespace'] = namespace

        log.info("Setting lock to '{}' for bucket '{}'".format(
            is_locked, bucket_name))

        return self.conn.put(
            'object/bucket/{}/lock/{}'.format(bucket_name, json.dumps(is_locked)),
            json_payload=payload)

    def set_quota(self, bucket_name, block_size, notification_size, namespace=None):
        """
        Updates the quota for the specified bucket. The payload specifies a limit
        at which a notification will be raised in the event log and a limit at
        which access will be blocked.

        Both notification and block values must be supplied. If you do not want
        to define one of them, you can set its value to -1. You cannot set both
        values to -1 using this API. To set both notification and block values
        to -1, use the delete quota API.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param bucket_name: Name of the bucket for which the quota is to be
        updated
        :param block_size: Block size in GB. Cannot be less than 1GB or use
        decimal values. Can be set to -1 to indicate quota value not defined
        :param notification_size: Notification size in GB. Cannot be less than
        1GB or use decimal values. Can be set to -1 to indicate quota value not
        defined
        :param namespace: Namespace to which this bucket belongs
        """
        payload = {
            "blockSize": block_size,
            "notificationSize": notification_size
        }

        if namespace:
            payload['namespace'] = namespace

        log.info("Updating quota for bucket '{}'".format(bucket_name))
        return self.conn.put(
            'object/bucket/{0}/quota'.format(bucket_name),
            json_payload=payload)

    def get_quota(self, bucket_name, namespace=None):
        """
        Gets the quota for the given bucket and namespace. The namespace with
        which the bucket is associated can be specified as a query parameter.

        A value of -1 for the block or notification quota value indicates that
        no quota has been defined.

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
        msg = "Getting quota for bucket '{}'".format(bucket_name)
        url = 'object/bucket/{}/quota'.format(bucket_name)

        if namespace:
            url += '?namespace={}'.format(namespace)
            msg += " in namespace '{}'".format(namespace)

        log.info(msg)
        return self.conn.get(url)

    def delete_quota(self, bucket_name, namespace=None):
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

        log.info("Deleting quota for bucket '{}'".format(bucket_name))

        return self.conn.delete(
            url='object/bucket/{}/quota'.format(bucket_name),
            params=params
        )

    def get_acl(self, bucket_name, namespace=None):
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

        :param bucket_name: Name of the bucket.
        :param namespace: Namespace with which bucket is associated. If it is
        null, the current user's namespace is used.
        """
        params = None
        if namespace:
            params = {'namespace': namespace}

        log.info("Getting ACL for bucket '{}'".format(bucket_name))

        return self.conn.get(
            'object/bucket/{}/acl'.format(bucket_name),
            params=params)

    def set_acl(self, bucket_name, namespace=None, owner=None, default_group=None,
                user_acl=None, group_acl=None, customgroup_acl=None):
        """
        Sets the ACL for the given bucket. If the buckets's namespace is not
        specified in the payload, the current user's namespace is used.

        Required role(s):

        This call has no restrictions

        :param bucket_name: The name of bucket used to set ACL information
        :param namespace: The namespace to which the bucket belongs. If not provided,
        then current user's namespace is used
        :param owner: The name of bucket owner
        :param default_group: The default group of the bucket
        :param user_acl: A collection of users and their corresponding permissions
        (e.g. `[{'permission': ['full_control'], 'user': 'myuser1'}]`)
        :param group_acl: A collection of groups and their corresponding permissions
        (e.g. `[{'permission': ['read'], 'group': 'public'}]`)
        :param customgroup_acl: A collection of custom groups and their corresponding permissions
        (e.g. `[{'permission': ['delete', 'read', 'write'], 'customgroup': 'cgroup1'}]`)
        """
        payload = {
            "bucket": bucket_name,
            "acl": {}
        }

        if namespace:
            payload['namespace'] = namespace
        if owner:
            payload['acl']['owner'] = owner
        if default_group:
            payload['acl']['default_group'] = default_group
        if user_acl:
            payload['acl']['user_acl'] = user_acl
        if group_acl:
            payload['acl']['group_acl'] = group_acl
        if customgroup_acl:
            payload['acl']['customgroup_acl'] = customgroup_acl

        log.info("Setting ACL for bucket '{}'".format(bucket_name))
        self.conn.put(
            'object/bucket/{}/acl'.format(bucket_name),
            json_payload=payload)

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
        return self.conn.get('object/bucket/acl/permissions')

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
        return self.conn.get('object/bucket/acl/groups')

    def get_metadata(self, bucket_name, head_type, namespace=None):
        """
        Fetch a page of head-specific metadata for the specified bucket

        Required Role(s):

        This call has no restrictions.

        Example JSON result from the API:

        {
            'metadata': [
                {'name': 'key1', 'value': 'value1'},
                {'name': 'key2', 'value': 'value2'}
            ],
            'head_type': 'S3'
        }

        :param bucket_name: Name of the bucket for which the default group
        is to be updated
        :param head_type: the head-type of the metadata to be queried (HDFS,
        S3, etc)
        :param namespace: Namespace with which bucket is associated. If it is
        null, the current user's namespace is used
        """
        params = {}
        if namespace:
            params['namespace'] = namespace
        if head_type:
            params['headType'] = head_type

        log.info("Getting metadata for bucket '{}'".format(bucket_name))
        return self.conn.get(
            'object/bucket/{}/metadata'.format(bucket_name),
            params=params)

    def set_metadata(self, bucket_name, metadata_key, metadata_value, head_type,
                     namespace=None):
        """
        Persist additional head metadata for the bucket

        Required Role(s):

        This call has no restrictions.

        Example JSON result from the API:

        :param bucket_name: Name of the bucket for which the metadata is to be added
        :param metadata_key: Metadata key to be added
        :param metadata_value: Metadata value to be added
        :param head_type: the head-type of the metadata to be added (HDFS,
        S3, etc)
        :param namespace: Namespace with which bucket is associated. If it is
        null, the current user's namespace is used
        """
        payload = {
            "head_type": head_type,
            "metadata": [
                {
                    "name": metadata_key,
                    "value": metadata_value
                }
            ]
        }
        url = 'object/bucket/{}/metadata'.format(bucket_name)
        if namespace:
            url += '?namespace={}'.format(namespace)
            payload['namespace'] = namespace

        log.info("Adding metadata to bucket '{}'".format(bucket_name))
        return self.conn.put(url, json_payload=payload)

    def delete_metadata(self, bucket_name, head_type, namespace=None):
        """
        Delete a page of head metadata for the specified bucket

        Required Role(s):

        This call has no restrictions.

        Example JSON result from the API:

        :param bucket_name: name of the bucket for which the metadata is to be removed
        :param head_type: the head-type of the metadata to be removed (HDFS, S3, etc)
        :param namespace: Namespace with which bucket is associated. If it is
        null, the current user's namespace is used
        """
        params = {'headType': head_type}
        if namespace:
            params['namespace'] = namespace

        log.info("Deleting metadata for bucket '{}', head '{}'".format(bucket_name, head_type))
        return self.conn.delete(
            'object/bucket/{}/metadata'.format(bucket_name),
            params=params)

    def get_system_metadata_keys(self):
        """
        Lists the system metadata keys available.

        Required Role(s):

        This call has no restrictions.

        Example JSON result from the API:

        ...
        """
        log.info('Listing the system metadata keys available')
        return self.conn.get('object/bucket/searchmetadata')

    def disable_search_metadata(self, bucket_name, namespace=None):
        """
        Disables the metadata search functionality for a bucket.

        Required Role(s):

        This call has no restrictions.

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param bucket_name: Bucket name for which metadata search mode will
        be disabled
        :param namespace: Namespace associated. If it is null, then current
        user's namespace is used
        """
        params = None
        if namespace:
            params = {'namespace': namespace}

        log.info("Disabling search metadata functionality for bucket '{}'".format(bucket_name))

        return self.conn.delete(
            'object/bucket/{}/searchmetadata'.format(bucket_name),
            params=params)
