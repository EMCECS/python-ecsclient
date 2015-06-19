# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class Namespace:
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_namespaces(self):
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

        return self.conn.get(url='object/namespaces')

    def get_namespace(self, namespace):
        """
        Gets the details for the given namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'default_data_services_vpool': u'urn: storageos: ReplicationGroupInfo: 4ea1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global',
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

        param: namespace: Namespace identifier for which details needs to
        be retrieved.
        """

        return self.conn.get(
            url='object/namespaces/namespace/{0}'.format(namespace))

    def get_retention_classes(self, namespace):
        """
        Gets the list of retention classes for the specified namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {u'retention_class': []}

        param: namespace: Namespace identifier for which retention classes
        needs to retrieved
        """

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

        param: namespace: Namespace for which retention period needs to
        be retrieved
        param: name: Class name for which retention period needs to
        be retrieved
        """

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

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        param: namespace: Namespace identifier for which retention class needs
        to be created.
        param: name: Name of the retention class
        param: period: Period of the retention class in seconds
        """

        payload = {
            "name": name,
            "period": period
        }

        return self.conn.post(
            url='object/namespaces/namespace/{0}/retention'.format(
                namespace), json_payload=payload)

    def update_retention_class(self, name, period, namespace):
        """
        Updates the retention class details for a specified retention class
        for a namespace.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        param: namespace: Namespace identifier for which retention class needs
        to be retrieved.
        param: name: Retention class name for which details needs to updated.
        param: period: A new period value for class in seconds
        """

        payload = {
            "period": period
        }

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

        param: namespace: Namespace identifier for which namespace quota
        details needs to retrieved.
        """

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

        param: namespace: Namespace identifier for which namespace quota
        details need to be updated.
        param: block_size: Block size in GB.
        param: notification_size: Notification size in GB.
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

        return self.conn.put(
            url='object/namespaces/namespace/{0}/quota'.format(
                namespace), json_payload=payload)
