import logging

log = logging.getLogger(__name__)


class Namespace(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def list(self):
        """
        Gets the identifiers for all configured namespaces.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'namespace': [
                {
                    u'link': {
                        u'href': u'/object/namespaces/namespace/namespace1',
                        u'rel': u'self'
                    },
                    u'name': u'namespace1',
                    u'id': u'namespace1'
                }
            ]
        }
        """
        log.info("Getting all namespaces")
        return self.conn.get(url='object/namespaces')

    def get(self, namespace):
        """
        Gets the details for the given namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'default_data_services_vpool':
                u'urn: storageos: ReplicationGroupInfo:
                    4ea1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global',
            u'remote': None,
            u'name': u'namespace1',
            u'tags': [

            ],
            u'namespace_admins': u'someone@email.com',
            u'user_mapping': [

            ],
            u'global': None,
            u'disallowed_vpools_list': [

            ],
            u'vdc': None,
            u'inactive': False,
            u'link': {
                u'href': u'/object/namespaces/namespace/namespace1',
                u'rel': u'self'
            },
            u'allowed_vpools_list': [

            ],
            u'id': u'namespace1'
        }

        :param namespace: Namespace identifier for which details needs to
        be retrieved.
        """
        log.info("Getting info for namespace '{0}'".format(namespace))

        return self.conn.get(
            url='object/namespaces/namespace/{0}'.format(namespace))

    def create(self, name, default_object_project=None, default_data_services_vpool=None,
               default_bucket_block_size=None, allowed_vpools_list=[], disallowed_vpools_list=[],
               namespace_admins=None, external_group_admins=None, user_mapping=[],
               is_encryption_enabled=False, is_stale_allowed=False, is_compliance_enabled=False):
        """
        Creates a namespace with the given details

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
          "namespace": {
            "id": "jt_namespace2",
            "inactive": "false",
            "isStaleAllowed": "true",
            "link": {
              "-rel": "self",
              "-href": "/object/namespaces/namespace/jt_namespace2"
            },
            "name": "jt_namespace2",
            "namespace_admins": "admin1,admin2,admin3",
            "user_mapping": [
              {
                "attributes": {
                  "attribute": [
                    {
                      "key": "key1",
                      "value": "value1"
                    },
                    {
                      "key": "key2",
                      "value": "value2"
                    }
                  ]
                },
                "domain": "jt_domain",
                "groups": { "group": "group1" }
              },
              {
                "attributes": {
                  "attribute": [
                    {
                      "key": "key2_1",
                      "value": "value2_1"
                    },
                    {
                      "key": "key2_2",
                      "value": "value2_2"
                    }
                  ]
                },
                "domain": "jt_domain_2",
                "groups": { "group": "group2" }
              }
            ]
          }
        }

        :param name: User provided namespace (verified unique). Cannot include dots or slashes (.|/) in the name
        :param default_object_project: Default project id for this tenant when creating buckets
        :param default_data_services_vpool: Default replication group identifier for this tenant when creating buckets
        :param default_bucket_block_size: Default bucket quota size
        :param allowed_vpools_list: List of replication groups that are allowed to create buckets on the corresponding
        namespace
        :param disallowed_vpools_list: List of replication groups that are not allowed to create buckets on the
        corresponding namespace
        :param namespace_admins: Comma separated list of namespace admins
        :param external_group_admins: List of groups from AD Server
        :param user_mapping: List of user mapping objects
        :param is_encryption_enabled: Flag to enable encryption for the namespace
        :param is_stale_allowed: Flag to allow stale data within the namespace
        :param is_compliance_enabled: Flag to enable namespace compliance
        :returns The namespace created
        """
        payload = {
            "namespace": name,
            "default_object_project": default_object_project,
            "default_data_services_vpool": default_data_services_vpool,
            "allowed_vpools_list": allowed_vpools_list,
            "disallowed_vpools_list": disallowed_vpools_list,
            "namespace_admins": namespace_admins,
            "user_mapping": user_mapping,
            "is_encryption_enabled": is_encryption_enabled,
            "default_bucket_block_size": default_bucket_block_size,
            "external_group_admins": external_group_admins,
            "is_stale_allowed": is_stale_allowed,
            "compliance_enabled": is_compliance_enabled
        }
        log.info("Creating namespace '{0}'".format(name))
        return self.conn.post('object/namespaces/namespace', json_payload=payload)

    def update(self, namespace_id, default_data_services_vpool=None, vpools_added_to_allowed_vpools_list=[],
               vpools_added_to_disallowed_vpools_list=[], vpools_removed_from_allowed_vpools_list=[],
               vpools_removed_from_disallowed_vpools_list=[], namespace_admins=None, user_mapping=None,
               default_bucket_block_size=None, external_group_admins=None, is_encryption_enabled=None,
               is_stale_allowed=None):
        """
        Updates namespace details like replication group list, namespace admins and user mappings.
        Replication group can be:
            - Added to allowed or disallowed replication group list
            - Removed from allowed or disallowed replication group list

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param namespace_id: Namespace identifier whose details needs to be updated
        :param default_data_services_vpool: Default replication group identifier when creating buckets
        :param vpools_added_to_allowed_vpools_list: List of replication group identifier which will be added in the
        allowed List for allowing namespace access
        :param vpools_added_to_disallowed_vpools_list: List of replication group identifier which will be added in the
        disallowed list for prohibiting namespace access
        :param vpools_removed_from_allowed_vpools_list: List of replication group identifier which will be removed
        from allowed list
        :param vpools_removed_from_disallowed_vpools_list: List of replication group identifier which will be removed
        from disallowed list for removing their prohibition namespace access
        :param namespace_admins: Comma separated list of namespace admins
        :param user_mapping: List of user mapping objects
        :param default_bucket_block_size: Default bucket quota size
        :param external_group_admins: List of groups from AD Server
        :param is_encryption_enabled: Update encryption for the namespace. If null then encryption will not be updated.
        :param is_stale_allowed: Flag to allow stale data within the namespace. If null then stale allowance will not be
        updated
        """
        payload = {
            "default_data_services_vpool": default_data_services_vpool,
            "vpools_added_to_allowed_vpools_list": vpools_added_to_allowed_vpools_list,
            "vpools_added_to_disallowed_vpools_list": vpools_added_to_disallowed_vpools_list,
            "vpools_removed_from_allowed_vpools_list": vpools_removed_from_allowed_vpools_list,
            "vpools_removed_from_disallowed_vpools_list": vpools_removed_from_disallowed_vpools_list,
            "namespace_admins": namespace_admins,
            "user_mapping": user_mapping,
            "default_bucket_block_size": default_bucket_block_size,
            "external_group_admins": external_group_admins,
            "is_encryption_enabled": is_encryption_enabled,
            "is_stale_allowed": is_stale_allowed
        }
        # FIXME: According to the API, this call should return the updated object, but it does not
        log.info("Updating namespace ID '{}'".format(namespace_id))
        return self.conn.put('object/namespaces/namespace/{}'.format(namespace_id), json_payload=payload)

    def delete(self, namespace_id):
        """
        Deactivates and deletes the given namespace and all associated user mappings.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param namespace_id: An active namespace identifier which needs to be deleted
        """
        log.info("Deleting namespace ID '{}'".format(namespace_id))
        # FIXME: This should be a DELETE request
        return self.conn.post('object/namespaces/namespace/{}/deactivate'.format(namespace_id))

    def get_retention_classes(self, namespace):
        """
        Gets the list of retention classes for the specified namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {u'retention_class': []}

        :param namespace: Namespace identifier for which retention classes
        needs to retrieved
        """
        log.info("Getting retention for namespace '{0}'".format(namespace))

        return self.conn.get(
            url='object/namespaces/namespace/{0}/retention'.format(namespace))

    def get_retention_class(self, name, namespace):
        """
        Gets the retention period for the given namespace and retention class.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            "name": "class_9cc8777c-bce0-11e4-8580-0050569c6fd7",
            "period": 2
        }

        :param name: Class name for which retention period needs to
        be retrieved
        :param namespace: Namespace for which retention period needs to
        be retrieved
        """
        log.info("Getting retention '{0}' in ns {1}".format(name, namespace))

        return self.conn.get(
            url='object/namespaces/namespace/{0}/retention/{1}'.format(
                namespace, name))

    def create_retention_class(self, name, period, namespace):
        """
        Creates a retention class for the specified namespace. The method
        payload specifies the retention class details which define a name for
        the class and a retention period.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param name: Name of the retention class
        :param period: Period of the retention class in seconds
        :param namespace: Namespace identifier for which retention class needs
        to be created.
        """
        payload = {
            "name": name,
            "period": period
        }

        log.info("Creating retention '{0}' in ns {1}".format(name, namespace))

        return self.conn.post(
            url='object/namespaces/namespace/{0}/retention'.format(namespace),
            json_payload=payload
        )

    def update_retention_class(self, name, period, namespace):
        """
        Updates the retention class details for a specified retention class
        for a namespace.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param name: Retention class name for which details needs to updated.
        :param period: A new period value for class in seconds
        :param namespace: Namespace identifier for which retention class needs
        to be retrieved.
        """
        payload = {
            "period": period
        }

        log.info("Updating retention '{0}' in ns {1}: {2}".format(name,
                                                                  namespace,
                                                                  payload))
        return self.conn.put(
            url='object/namespaces/namespace/{0}/retention/{1}'.format(
                namespace, name), json_payload=payload)

    def get_namespace_quota(self, namespace):
        """
        Gets the namespace quota for a specified namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'blockSize': -1,
            u'notificationSize': -1,
            u'namespace': u'namespace1'
        }

        :param namespace: Namespace identifier for which namespace quota
        details needs to retrieved.
        """
        log.info("Getting quota for namespace '{0}'".format(namespace))

        return self.conn.get(
            url='object/namespaces/namespace/{0}/quota'.format(namespace))

    def update_namespace_quota(self, block_size, notification_size, namespace):
        """
        Updates the namespace quota for a specified namespace.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param block_size: Block size in GB.
        :param notification_size: Notification size in GB.
        :param namespace: Namespace identifier for which namespace quota
        details need to be updated.
        """
        # ----
        # Note
        # ----
        # These two params are what the ECS API docs state, however, every
        # other parameter is broken up into two word with an underscore
        # separating them, ie: block_size
        # I can't verify at the moment that this call works as is.
        payload = {
            "blockSize": block_size,
            "notificationSize": notification_size
        }

        log.info("Updating quota for namespace '{0}': {1}".format(namespace,
                                                                  payload))
        return self.conn.put(
            url='object/namespaces/namespace/{0}/quota'.format(namespace),
            json_payload=payload
        )
