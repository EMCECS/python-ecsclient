import logging

log = logging.getLogger(__name__)


class VirtualDataCenter(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def list(self):
        """
        Gets all details of all configured VDCs.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        SECURITY_ADMIN

        Example JSON result from the API:

        {
            u'vdc': [
                {
                    u'remote': None,
                    u'name': u'tiva01',
                    u'tags': [

                    ],
                    u'global': None,
                    u'interVdcEndPoints': u'192.29.3.48,
                    172.29.3.149,
                    172.29.3.150,
                    172.29.3.151,
                    172.29.3.152,
                    172.29.3.153,
                    172.29.3.154,
                    172.29.3.155',
                    u'vdcId': u'urn: storageos: VirtualDataCenterData:
                                a9faea85-d377-4a42-b5f1-fa15829f0c33',
                    u'vdc': None,
                    u'inactive': False,
                    u'link': {
                        u'href': u'/object/vdcs/vdc/tiva01',
                        u'rel': u'self'
                    },
                    u'secretKeys': u'55fmIFBniRuCBVx327Av',
                    u'vdcName': u'tiva01',
                    u'local': True,
                    u'id': u'urn: storageos: VirtualDataCenterData:
                                a9faea85-d377-4a42-b5f1-fa15829f0c33',
                    u'permanentlyFailed': False
                },
                {
                    u'remote': None,
                    u'name': u'tiva02',
                    u'tags': [

                    ],
                    u'global': None,
                    u'interVdcEndPoints': u'192.29.3.12,
                    172.29.3.213,
                    172.29.3.214,
                    172.29.3.215,
                    172.29.3.216,
                    172.29.3.217,
                    172.29.3.218,
                    172.29.3.219',
                    u'vdcId': u'urn: storageos: VirtualDataCenterData:
                                7d7d2ed5-e253-4be9-b8bb-5ff5b2697e6f',
                    u'vdc': None,
                    u'inactive': False,
                    u'link': {
                        u'href': u'/object/vdcs/vdc/tiva02',
                        u'rel': u'self'
                    },
                    u'secretKeys': u'99TilKh9aTwt9fLbCiKd',
                    u'vdcName': u'tiva02',
                    u'local': False,
                    u'id': u'urn: storageos: VirtualDataCenterData:
                                7d7d2ed5-e253-4be9-b8bb-5ff5b2697e6f',
                    u'permanentlyFailed': False
                }
            ]
        }
        """
        log.info('Listing VDCs')
        return self.conn.get('object/vdcs/vdc/list')

    def get(self, vdc_id=None, name=None):
        """
        Gets the details for a VDC by its ID or its name. Either of the two have to be set.
        If both are set, only the ID is used.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'remote': None,
            u'name': u'tiva01',
            u'tags': [

            ],
            u'global': None,
            u'interVdcEndPoints': u'192.29.3.48,
            172.29.3.149,
            172.29.3.150,
            172.29.3.151,
            172.29.3.152,
            172.29.3.153,
            172.29.3.154,
            172.29.3.155',
            u'vdcId': u'urn: storageos: VirtualDataCenterData:
                        a9faea85-d377-4a42-b5f1-fa15829f0c33',
            u'vdc': None,
            u'inactive': False,
            u'link': {
                u'href': u'/object/vdcs/vdc/tiva01',
                u'rel': u'self'
            },
            u'secretKeys': u'55fmIFBniRuCBVx327Av',
            u'vdcName': u'tiva01',
            u'local': True,
            u'id': u'urn: storageos: VirtualDataCenterData:
                        a9faea85-d377-4a42-b5f1-fa15829f0c33',
            u'permanentlyFailed': False
        }

        param: vdc_id: VDC identifier for which VDC Information is to be retrieved.
        param: name: VDC name for which VDC Information is to be retrieved.
        """
        if not vdc_id and not name:
            raise ValueError('Either the ID or the name have to be set.')

        if vdc_id:
            log.info("Getting VDC by ID '{}'".format(vdc_id))
            url = 'object/vdcs/vdcid/{}'.format(vdc_id)
        else:
            log.info("Getting VDC by name '{}'".format(name))
            url = 'object/vdcs/vdc/{}'.format(name)

        return self.conn.get(url)

    def get_local(self):
        """
        Gets the details for the local VDC.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        SECURITY_ADMIN

        Example JSON result from the API:

        {
            u'remote': None,
            u'name': u'tiva01',
            u'tags': [

            ],
            u'global': None,
            u'interVdcEndPoints': u'192.29.3.48,
            172.29.3.149,
            172.29.3.150,
            172.29.3.151,
            172.29.3.152,
            172.29.3.153,
            172.29.3.154,
            172.29.3.155',
            u'vdcId': u'urn: storageos: VirtualDataCenterData:
                        a9faea85-d377-4a42-b5f1-fa15829f0c33',
            u'vdc': None,
            u'inactive': False,
            u'link': {
                u'href': u'/object/vdcs/vdc/tiva01',
                u'rel': u'self'
            },
            u'secretKeys': u'55fmIFBniRuCBVx327Av',
            u'vdcName': u'tiva01',
            u'local': True,
            u'id': u'urn: storageos: VirtualDataCenterData:
                        a9faea85-d377-4a42-b5f1-fa15829f0c33',
            u'permanentlyFailed': False
        }
        """
        return self.get(name='local')

    def get_local_secret_key(self):
        """
        Gets the secret key for the local VDC.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {u'key': u'55fmIFBniRuCBVx327Av'}
        """
        log.info('Getting local VDC secret key')
        return self.conn.get('object/vdcs/vdc/local/secretkey')

    def update(self, vdc_name, inter_vdc_endpoints, secret_key, new_name=None,
               inter_vdc_cmd_endpoints=None, management_endpoints=None):
        """
        Update the attributes for the current VDC or a VDC which you want the
        current VDC to connect. Enables the name of the VDC, the end points
        that can be used to communicate with it, and a secret key used to
        encrypt traffic between VDCs to be set.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param vdc_name: VDC name for which mapping needs to be update
        :param new_name: Name of VDC to be updated (optional)
        :param inter_vdc_endpoints: Endpoints for the VDC
        :param secret_key: Secret key to encrypt communication between VDC
        :param inter_vdc_cmd_endpoints: Control Plane endpoints for the VDC (optional)
        :param management_endpoints: The management end points for the VDC (optional)
        """
        if not new_name:
            new_name = vdc_name

        payload = {
            'vdcName': new_name,
            'interVdcEndPoints': inter_vdc_endpoints,
            'secretKeys': secret_key
        }
        if inter_vdc_cmd_endpoints:
            payload['interVdcCmdEndPoints'] = inter_vdc_cmd_endpoints
        if management_endpoints:
            payload['managementEndPoints'] = management_endpoints

        log.info("Updating the VDC with name '{}'".format(vdc_name))
        return self.conn.put('object/vdcs/vdc/{}'.format(vdc_name), json_payload=payload)

    def delete(self, vdc_id):
        """
        Deactivates and deletes a VDC. Enables attributes for the current VDC
        to be deleted and enables information held by a VDC about other VDCs
        to be deleted.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param vdc_id: VDC identifier for which VDC Information needs to be
        deleted
        """
        log.info("Deleting VDC '{}'".format(vdc_id))

        return self.conn.post('object/vdcs/vdc/{}/deactivate'.format(vdc_id))
