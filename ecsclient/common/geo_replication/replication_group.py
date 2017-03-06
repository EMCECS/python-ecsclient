import logging

log = logging.getLogger(__name__)


class ReplicationGroup(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def list(self):
        """
        Lists all configured replication groups.

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
                            u'name': u'urn: storageos: VirtualDataCenterData:
                                    7d7d2ed5-e253-4be9-b8bb-5ff5b2697e6f',
                            u'value': u'urn: storageos: VirtualArray:
                                    527caf55-e989-4485-b92d-ce465d20dd56'
                        }
                    ],
                    u'id': u'urn: storageos: ReplicationGroupInfo:
                                61f20dc2-a862-4935-9110-45030f0fe17c: global',
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
                            u'name': u'urn: storageos: VirtualDataCenterData:
                                        a9faea85-d377-4a42-b5f1-fa15829f0c33',
                            u'value': u'urn: storageos: VirtualArray:
                                        3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37'
                        }
                    ],
                    u'id': u'urn: storageos: ReplicationGroupInfo:
                            c2b0d3c4-c778-4a24-8da5-6a89784c4eeb: global',
                    u'description': u''
                }
            ]
        }
        """
        log.info("Listing replication groups")
        return self.conn.get('vdc/data-service/vpools')

    def get(self, replication_group_id):
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
                    u'name': u'urn: storageos: VirtualDataCenterData:
                                a9faea85-d377-4a42-b5f1-fa15829f0c33',
                    u'value': u'urn: storageos: VirtualArray:
                                3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37'
                }
            ],
            u'id': u'urn: storageos: ReplicationGroupInfo:
                        c2b0d3c4-c778-4a24-8da5-6a89784c4eeb: global',
            u'description': u''
        }

        :param replication_group_id: Replication group identifier for which
        details needs to be retrieved
        """
        log.info("Getting replication group with ID='{}'".format(replication_group_id))
        return self.conn.get('vdc/data-service/vpools/{0}'.format(replication_group_id))

    def update(self, replication_group_id, name=None, description=None,
               enable_rebalancing=None, allow_all_namespaces=None):
        """
        Updates the details for a replication group.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param replication_group_id: Replication group identifier for which details need to be updated
        :param name: New name for the replication group
        :param description: New description for the replication group
        :param enable_rebalancing: Set to True to enabled geo rebalancing. False to disable it.
        :param allow_all_namespaces: Allow all namespaces to update True/False
        """
        # Need to check these mandatory arguments, otherwise the API will complain
        if not name:
            ValueError('name argument must be set')
        if not description:
            ValueError('description argument must be set')
        if not allow_all_namespaces:
            ValueError('allow_all_namespaces argument must be set')

        payload = {
            'name': name,
            'description': description,
            'allowAllNamespaces': allow_all_namespaces
        }

        if enable_rebalancing:
            payload['enable_rebalancing'] = enable_rebalancing

        log.info("Updating replication group with ID='{}'".format(replication_group_id))
        return self.conn.put('vdc/data-service/vpools/{}'.format(replication_group_id), json_payload=payload)

    def create(self, name, zone_mappings, description=None, enable_rebalancing=None, allow_all_namespaces=None,
               is_full_rep=None):
        """
        Creates a replication group that includes the specified storage pools (VDC:storage pool tuple).

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            u'isAllowAllNamespaces': True,
            u'remote': None,
            u'name': u'us2',
            u'global': None,
            u'vdc': None,
            u'varrayMappings': [
                {
                    u'name': u'urn: storageos: VirtualDataCenterData:
                                a9faea85-d377-4a42-b5f1-fa15829f0c33',
                    u'value': u'urn: storageos: VirtualArray:
                                3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37'
                }
            ],
            u'id': u'urn: storageos: ReplicationGroupInfo:
                        c2b0d3c4-c778-4a24-8da5-6a89784c4eeb: global',
            u'description': u''
        }

        :param name: Unique name identifying this classification of replication group
        :param zone_mappings: Mappings between Virtual Data Centers and Storage Pools. List of tuples with the
        following format: (vdc_id, storage_pool_id)
        :param description: Description of this replication group
        :param enable_rebalancing: Set to True to enabled geo rebalancing. False to disable it.
        :param allow_all_namespaces: Allow all namespaces to update True/False
        :param is_full_rep: Full replication flag
        """
        payload = {
            "name": name,
            "description": description,
            "isAllowAllNamespaces": allow_all_namespaces,
            "enable_rebalancing": enable_rebalancing,
            "isFullRep": is_full_rep,
            "zone_mappings": []
        }

        if not zone_mappings:
            raise ValueError('zone_mappings cannot be empty')

        try:
            for mapping in zone_mappings:
                payload['zone_mappings'].append({
                    "name": mapping[0],
                    "value": mapping[1]
                })
        except:
            raise ValueError('zone_mappings does not have the correct format')

        log.info("Creating replication group with name='{}'".format(name))
        return self.conn.post('vdc/data-service/vpools', json_payload=payload)

    def delete(self, replication_group_id):
        """
        Deletes a specified replication group

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param replication_group_id: Replication group to be deleted
        """
        log.info("Deleting replication group with ID='{}'".format(replication_group_id))
        return self.conn.post('vdc/data-service/vpools/{}/deactivate'.format(replication_group_id))

    def add_storage_pool(self, replication_group_id, vdc_id, storage_pool_id):
        """
        Adds a storage pool (as VDC:storage pool tuple) to the specified replication group.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
          "data_service_vpool_varrays": {
            "mappings": {
              "name": "vdc_id",
              "value": "StoragePool_Id"
            }
          }
        }

        :param replication_group_id: Replication group identifier for which storage pool needs to be added
        :param vdc_id: Virtual data center ID
        :param storage_pool_id: Storage pool ID
        """
        payload = {
            "mappings": [
                {
                    "name": vdc_id,
                    "value": storage_pool_id
                }
            ]
        }
        log.info("Adding the storage pool '{}' to the replication group '{}'".format(
            storage_pool_id, replication_group_id))
        return self.conn.put('vdc/data-service/vpools/{}/addvarrays'.format(replication_group_id),
                             json_payload=payload)

    def remove_storage_pool(self, replication_group_id, vdc_id, storage_pool_id):
        """
        Deletes a storage pool (VDC:storage pool tuple) from a specified replication group.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param replication_group_id: Replication group identifier for which storage pool needs to be removed
        :param vdc_id: Virtual data center ID
        :param storage_pool_id: Storage pool ID
        """
        payload = {
            "mappings": [
                {
                    "name": vdc_id,
                    "value": storage_pool_id
                }
            ]
        }
        log.info("Removing the storage pool '{}' from the replication group '{}'".format(
            storage_pool_id, replication_group_id))
        return self.conn.put('vdc/data-service/vpools/{}/removevarrays'.format(replication_group_id),
                             json_payload=payload)
