# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class StoragePool(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_virtual_array(self, storage_pool_id):
        """
        Gets the details for the specified storage pool.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'isProtected': False,
            u'id': u'urn: storageos: VirtualArray:
                    3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37',
            u'name': u'storagepool1'
        }

        :param storage_pool_id: Storage pool identifier to be retrieved
        """
        log.info("Getting varray '{0}'".format(storage_pool_id))

        return self.conn.get(
            url='vdc/data-services/varrays/{0}'.format(storage_pool_id))

    def get_virtual_arrays(self, vdc_id=None):
        """
        Gets a list of storage pools from the local VDC.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'varray': [
                {
                    u'isProtected': False,
                    u'id': u'urn: storageos: VirtualArray:
                            3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37',
                    u'name': u'storagepool1'
                }
            ]
        }

        :param vdc_id: Virtual data center identifier for which list of
        storage pool is to be retrieved
        """
        params = None

        if vdc_id:
            params = {'vdc-id': vdc_id}

        log.info("Getting varrays for VDC: {0}".format(params))

        return self.conn.get(url='vdc/data-services/varrays', params=params)
