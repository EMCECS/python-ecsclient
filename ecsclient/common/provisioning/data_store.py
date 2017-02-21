# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class DataStore(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_data_stores(self):
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
        log.info("Getting all data stores")
        return self.conn.get(url='vdc/data-stores')

    def get_data_store(self, data_store_id):
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
        log.info("Getting commodity store '{0}'".format(data_store_id))

        return self.conn.get(
            url='vdc/data-stores/commodity/{0}'.format(data_store_id))

    def get_data_stores_by_storage_pool_id(self, storage_pool_id):
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
        log.info("Getting commodity stores for varray '{0}'"
                 .format(storage_pool_id))

        return self.conn.get(
            url='vdc/data-stores/commodity/search/varray/{0}'.format(
                storage_pool_id))

    def create_data_store(self, name, description, node_id, storage_pool_id):
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
            u'tasks': {
                u'task': {
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
            }
        }

        :param name: User provided name (not verified or unique)
        :param description: User provided description (not verified or unique)
        :param node_id: IP address for the commodity node
        :param storage_pool_id: Desired storage pool ID for creating data store
        """
        payload = {
            "name": name,
            "description": description,
            "nodeId": node_id,
            "virtual_array": storage_pool_id
        }

        log.info("Creating data store '{0}': {1}".format(name, payload))

        return self.conn.post(
            url='vdc/data-stores/commodity',
            json_payload=payload
        )
