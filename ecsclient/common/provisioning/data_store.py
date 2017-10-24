import logging

log = logging.getLogger(__name__)


class DataStore(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def list(self):
        """
        Gets list of configured commodity or filesystem data stores.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'data_store': [
                {
                    u'link': {
                        u'href': u'/vdc/data-stores/commodity/192.29.3.51',
                        u'rel': u'self'
                    },
                    u'name': u'tiva01-r01-04.blah01s1.rraas-ops.com',
                    u'resource_type': u'commodity',
                    u'id': u'192.29.3.51'
                },
                {
                    u'link': {
                        u'href': u'/vdc/data-stores/commodity/192.29.3.54',
                        u'rel': u'self'
                    },
                    u'name': u'tiva01-r01-07.blah02s2.rraas-ops.com',
                    u'resource_type': u'commodity',
                    u'id': u'192.29.3.54'
                }
            ]
        }
        """
        log.info("Listing data stores")
        return self.conn.get(url='vdc/data-stores')

    def get(self, data_store_id):
        """
        Gets the details for a commodity data store.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'remote': None,
            u'name': u'tiva01-r01-04.blah01s1.rraas-ops.com',
            u'tags': [],
            u'device_state': u'readytouse',
            u'global': None,
            u'creation_time': 1432185210000,
            u'device_info': u'',
            u'used_gb': 1073,
            u'usable_gb': 334800,
            u'vdc': None,
            u'link': {
                u'href': u'/vdc/object-pools/172.29.3.151',
                u'rel': u'self'
            },
            u'free_gb': 333727,
            u'varray': u'urn: storageos: VirtualArray:
                        3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37',
            u'id': u'192.29.3.51',
            u'description': u''
        }

        :param data_store_id: Identifier of the data store
        """
        log.info("Getting commodity store ID '{}'".format(data_store_id))
        return self.conn.get('vdc/data-stores/commodity/{}'.format(data_store_id))

    def get_by_storage_pool(self, storage_pool_id):
        """
        Gets the list of details of commodity data stores associated with a
        storage pool.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'commodity_data_store': [
                {
                    u'remote': None,
                    u'name': u'tiva01-r01-04.blah01s1.rraas-ops.com',
                    u'tags': [],
                    u'device_state': u'readytouse',
                    u'global': None,
                    u'creation_time': 1432185210000,
                    u'device_info': u'',
                    u'used_gb': 318025,
                    u'usable_gb': 334800,
                    u'vdc': None,
                    u'link': {
                        u'href': u'/vdc/object-pools/192.29.3.51',
                        u'rel': u'self'
                    },
                    u'free_gb': 16775,
                    u'varray': u'urn: storageos: VirtualArray:
                                3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37',
                    u'id': u'192.29.3.51',
                    u'description': u''
                },
                {
                    u'remote': None,
                    u'name': u'tiva01-r01-07.blah02s2.rraas-ops.com',
                    u'tags': [

                    ],
                    u'device_state': u'readytouse',
                    u'global': None,
                    u'creation_time': 1432185214000,
                    u'device_info': u'',
                    u'used_gb': 318026,
                    u'usable_gb': 334800,
                    u'vdc': None,
                    u'link': {
                        u'href': u'/vdc/object-pools/192.29.3.54',
                        u'rel': u'self'
                    },
                    u'free_gb': 16774,
                    u'varray': u'urn: storageos: VirtualArray:
                                3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37',
                    u'id': u'192.29.3.54',
                    u'description': u''
                }
            ]
        }

        :param storage_pool_id: Identifier of the storage pool
        """
        log.info("Getting commodity stores for storage pool ID '{}'"
                 .format(storage_pool_id))
        return self.conn.get('vdc/data-stores/commodity/search/varray/{0}'.format(storage_pool_id))

    def create(self, name, description, node_id, storage_pool_id):
        """
        NOTE: This is an asychronous operation that returns a task object.

        Creates one or more new commodity data stores. A data store represents
        a commodity node providing backing storage for the object store. On
        creating, the data store is associated with the storage pool specified
        in the request.

        Note that the data store creation is an asynchronous operation so a
        successful invocation of this request does not necessarily mean that
        the creation has completed.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            u'task': [
                {
                    u'resource': {
                        u'name': u'Sample_Volume',
                        u'id': u'urn: storageos:
                                Volume:5ba5b8d8-a0ca-4827-84f9-c1fef57733f5:',
                        u'link': {
                            u'rel': u'self',
                            u'href': u'/block/volumes/urn: storageos: Volume:
                                      5ba5b8d8-a0ca-4827-84f9-c1fef57733f5:'
                        }
                    },
                    u'state': u'pending',
                    u'start_time': u'1379398608574',
                    u'op_id': u'265cf333-76a1-4129-903e-fac63f9b4adc',
                    u'link': {
                        u'rel': u'self',
                        u'href': u'/block/volumes/urn: storageos: Volume:
                                  5ba5b8d8-a0ca-4827-84f9-c1fef57733f5:
                                  /tasks/265cf333-76a1-4129-903e-fac63f9b4adc'
                    }
                }
            ]
        }


        :param name: User provided name (not verified or unique)
        :param description: User provided description (not verified or unique)
        :param node_id: ID of the commodity node
        :param storage_pool_id: Desired storage pool ID for creating data store
        :returns a task object
        """
        payload = {"nodes": [
            {
                "name": name,
                "description": description,
                "nodeId": node_id,
                "virtual_array": storage_pool_id
            }
        ]}

        log.info("Creating data store '{}': {}".format(name, payload))
        return self.conn.post('vdc/data-stores/commodity', json_payload=payload)

    def delete(self, data_store_id):
        """
        Deactivates the commodity node and data store

        Note: Storage will be deleted if it was allocated with the data store.

        Note: Data store deletion is an asynchronous operation, so a successful invocation
        of this request does not necessarily mean that the deletion has completed.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            u'task': [
                {
                    u'resource': {
                        u'name': u'Sample_Volume',
                        u'id': u'urn: storageos:
                                Volume:5ba5b8d8-a0ca-4827-84f9-c1fef57733f5:',
                        u'link': {
                            u'rel': u'self',
                            u'href': u'/block/volumes/urn: storageos: Volume:
                                      5ba5b8d8-a0ca-4827-84f9-c1fef57733f5:'
                        }
                    },
                    u'state': u'pending',
                    u'start_time': u'1379398608574',
                    u'op_id': u'265cf333-76a1-4129-903e-fac63f9b4adc',
                    u'link': {
                        u'rel': u'self',
                        u'href': u'/block/volumes/urn: storageos: Volume:
                                  5ba5b8d8-a0ca-4827-84f9-c1fef57733f5:
                                  /tasks/265cf333-76a1-4129-903e-fac63f9b4adc'
                    }
                }
            ]
        }

        :param data_store_id: Identifier of data store to delete
        :return: a task object
        """
        log.info("Deleting data store ID '{}'".format(data_store_id))
        return self.conn.post('vdc/data-stores/{}/deactivate'.format(data_store_id))

    def get_task(self, data_store_id, op_id):
        """
        Get the task with the given ID for a specific data store.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'op_id': u'CREATE',
            u'resource': {
                u'link': {u'href': u'/vdc/object-pools/10.1.83.70', u'rel': u'self'},
                u'id': u'10.1.83.70',
                u'name': u'10.1.83.70'
            },
            u'name': u'CREATE',
            u'global': None,
            u'associated_resources': [],
            u'state': u'pending',
            u'vdc': None,
            u'link': {u'href': u'/vdc/data-stores/10.1.83.70/tasks/CREATE',
                      u'rel': u'self'},
            u'remote': None,
            u'restLink': None
        }

        :param data_store_id: Identifier for the data store to query
        :param op_id: Identifier for the task operation of the data store
        """
        log.info("Getting tasks for data store ID '{}'".format(data_store_id))
        return self.conn.get('vdc/data-stores/{}/tasks/{}'.format(data_store_id, op_id))
