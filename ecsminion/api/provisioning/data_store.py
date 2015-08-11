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

    def get_data_store_list(self):
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

    def get_commodity_data_store_associated_wth_storage_pool(
            self, commodity_node_id):
        """
        Gets the details for a commodity data store.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'remote': None,
            u'name': u'tiva01-r01-04.blah01s1.rraas-ops.com',
            u'tags': [

            ],
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

        :param commodity_node_id: Identifier of the data store
        """
        log.info("Getting commodity store '{0}'".format(commodity_node_id))

        return self.conn.get(
            url='vdc/data-stores/commodity/{0}'.format(commodity_node_id))

    def get_commodity_data_store_associated_wth_varray(
            self, storage_pool_id):
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
                    u'tags': [

                    ],
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
        log.info("Getting commodity store for varray '{0}'".format(
                                                              storage_pool_id))
        return self.conn.get(
            url='vdc/data-stores/commodity/search/varray/{0}'.format(
                storage_pool_id))
