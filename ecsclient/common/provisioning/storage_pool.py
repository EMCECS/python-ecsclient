import logging

log = logging.getLogger(__name__)


class StoragePool(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get(self, storage_pool_id):
        """
        Gets the details for the specified storage pool.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            'isProtected': False,
            'isColdStorageEnabled': False,
            'id': 'urn: storageos: VirtualArray:
                    3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37',
            'name': 'storagepool1'
        }

        :param storage_pool_id: Storage pool identifier to be retrieved
        """
        log.info("Getting storage pool '{}'".format(storage_pool_id))
        return self.conn.get('vdc/data-services/varrays/{}'.format(storage_pool_id))

    def list(self, vdc_id=None):
        """
        Gets a list of storage pools from the local VDC.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            'varray': [
                {
                    'isProtected': False,
                    'isColdStorageEnabled': False,
                    'id': 'urn: storageos: VirtualArray:
                            3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37',
                    'name': 'storagepool1'
                },
                {
                    'isProtected': True,
                    'isColdStorageEnabled': False,
                    'id': 'urn: storageos: VirtualArray:
                            c7fc54dc-6616-4b7e-a86c-0210ef9a8804',
                    'name': 'storagepool2'
                }
            ]
        }

        :param vdc_id: Virtual data center identifier for which list of storage pool is to be retrieved
        """
        msg = "Listing storage pools"
        params = None
        if vdc_id:
            params = {'vdc-id': vdc_id}
            msg += " for VDC '{}'".format(vdc_id)
        log.info(msg)
        return self.conn.get('vdc/data-services/varrays', params=params)

    def create(self, name, description=None, is_protected=False, is_cold_storage_enabled=False):
        """
        Create a storage pool with the specified details.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            'id': 'urn:storageos:VirtualArray:dd751e72-142-598-b4f833e93b61',
            'name': 'storage_pool',
            'isProtected': False,
            'isColdStorageEnabled': False
        }

        :param name: Storage pool name
        :param description: Storage pool description
        :param is_protected: Set to True to enable storage pool protection, False otherwise
        :param is_cold_storage_enabled: Set to True to enable cold storage, False otherwise
        """
        if not description:
            description = name

        payload = {
            "name": name,
            "description": description,
            "isProtected": is_protected,
            "isColdStorageEnabled": is_cold_storage_enabled
        }
        log.info("Creating storage pool '{}'".format(name))
        return self.conn.post('vdc/data-services/varrays', json_payload=payload)

    def update(self, storage_pool_id, name=None, is_protected=None):
        """
        Updates storage pool for the specified identifier.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            'id': 'urn:storageos:VirtualArray:82cf257b-0782-433c-92ca-2ee6161b917e',
            'name': 'CommodityvPool',
            'description': 'desc',
            'isProtected': True,
            'isColdStorageEnabled': False
        }

        :param storage_pool_id: Storage pool identifier to be updated
        :param name: Name of virtual array to be updated
        :param is_protected: Set to True to enable storage pool protection, False otherwise
        """
        payload = {
            "name": name,
            "isProtected": is_protected
        }
        # FIXME: API throws error if 'isColdStorageEnabled' and 'description' fields are sent
        log.info("Updating storage pool ID '{}'".format(storage_pool_id))
        return self.conn.put('vdc/data-services/varrays/{}'.format(storage_pool_id),
                             json_payload=payload)

    def delete(self, storage_pool_id):
        """
        Deletes the storage pool for the specified identifier.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param storage_pool_id: storage pool identifier to be deleted
        """
        log.info("Deleting storage pool ID '{}'".format(storage_pool_id))
        return self.conn.delete('vdc/data-services/varrays/{}'.format(storage_pool_id))
