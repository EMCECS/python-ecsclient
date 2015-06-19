# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class ReplicationGroup:

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_replication_groups(self):
        """
        Gets the user lock state for the specified user belonging to the
        specified namespace (if provided).

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'data_service_vpool': [
                {
                    u'isAllowAllNamespaces': True,
                    u'remote': None,
                    u'name': u'us1',
                    u'tags': [

                    ],
                    u'global': None,
                    u'creation_time': 1434739694878,
                    u'vdc': None,
                    u'inactive': False,
                    u'varrayMappings': [
                        {
                            u'name': u'urn: storageos: VirtualDataCenterData: 7d7d2ed5-e253-4be9-b8bb-5ff5b2697e6f',
                            u'value': u'urn: storageos: VirtualArray: 527caf55-e989-4485-b92d-ce465d20dd56'
                        }
                    ],
                    u'id': u'urn: storageos: ReplicationGroupInfo: 61f20dc2-a862-4935-9110-45030f0fe17c: global',
                    u'description': u''
                },
                {
                    u'isAllowAllNamespaces': True,
                    u'remote': None,
                    u'name': u'us2',
                    u'tags': [

                    ],
                    u'global': None,
                    u'creation_time': 1434739694878,
                    u'vdc': None,
                    u'inactive': False,
                    u'varrayMappings': [
                        {
                            u'name': u'urn: storageos: VirtualDataCenterData: a9faea85-d377-4a42-b5f1-fa15829f0c33',
                            u'value': u'urn: storageos: VirtualArray: 3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37'
                        }
                    ],
                    u'id': u'urn: storageos: ReplicationGroupInfo: c2b0d3c4-c778-4a24-8da5-6a89784c4eeb: global',
                    u'description': u''
                }
            ]
        }
        """

        return self.conn.get(url='vdc/data-service/vpools')

    def get_replication_group(self, replication_group_id):
        """
        Gets the details for the specified replication group.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'isAllowAllNamespaces': True,
            u'remote': None,
            u'name': u'us2',
            u'tags': [

            ],
            u'global': None,
            u'creation_time': 1434740060384,
            u'vdc': None,
            u'inactive': False,
            u'varrayMappings': [
                {
                    u'name': u'urn: storageos: VirtualDataCenterData: a9faea85-d377-4a42-b5f1-fa15829f0c33',
                    u'value': u'urn: storageos: VirtualArray: 3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37'
                }
            ],
            u'id': u'urn: storageos: ReplicationGroupInfo: c2b0d3c4-c778-4a24-8da5-6a89784c4eeb: global',
            u'description': u''
        }

        param: replication_group_id: Replication group identifier for which
        details needs to be retrieved
        """

        return self.conn.get(
            url='vdc/data-service/vpools/{0}'.format(replication_group_id))

    def update_replication_group(self, uid, name, description,
                                 allow_all_namespaces=False):
        """
        Updates the name and description for a replication group.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param uid: User identifier for which local user information needs to
        be updated.
        :param name: New name fro the replication group
        :param description: New description for the replication group
        :param allow_all_namespaces: Allow all namespaces to update True/False
        """
        payload = {
            "name": name,
            "description": description,
            "allow_all_namespaces": allow_all_namespaces
        }

        return self.conn.put(
            url='vdc/data-service/vpools/{0}'.format(uid),
            json_payload=payload)
