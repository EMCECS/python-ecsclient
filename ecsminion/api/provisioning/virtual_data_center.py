# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class VirtualDataCenter:

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_all_vdcs(self):
        """
        Gets all details of all configured VDCs.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

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

        return self.conn.get(url='object/vdcs/vdc/list')

    def get_vdcs_by_id(self, vdc_id):
        """
        Gets all details of all configured VDCs.

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

        param: vdc_id: VDC identifier for which VDC Information is to be
        retrieved.
        """

        return self.conn.get(url='object/vdcs/vdcid/{0}'.format(vdc_id))

    def get_local_vdc(self):
        """
        Gets the details for the local VDC.

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
        """

        return self.conn.get(url='object/vdcs/vdc/local')

    def get_local_vdc_secret_key(self):
        """
        Gets the secret key for the local VDC.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {u'key': u'55fmIFBniRuCBVx327Av'}
        """

        return self.conn.get(url='object/vdcs/vdc/local/secretkey')

    def get_vdc_by_name(self, vdc_name):
        """
        Gets the details for a VDC the identify of which is specified by
        its name.

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

        param: vdc_name: VDC name for which VDC Information is to be retrieved
        """

        return self.conn.get(url='object/vdcs/vdc/{0}'.format(vdc_name))

    def insert_vdc_attributes(self, vdc_name, inter_vdc_end_point,
                              secret_key):
        """
        Insert the attributes for the current VDC or a VDC which you want the
        current VDC to connect. Enables the name of the VDC, the end points
        that can be used to communicate with it, and a secret key used to
        encrypt traffic between VDCs to be set.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param vdc_name: Name of VDC to be inserted
        :param inter_vdc_end_point: End points for the VDC
        :param secret_key: Secret key to encrypt communication between VDC
        """
        payload = {
            "vdc_name": vdc_name,
            "inter_vdc_end_point": inter_vdc_end_point,
            "secret_key": secret_key
        }

        return self.conn.put(
            url='object/vdcs/vdc/{0}'.format(vdc_name), json_payload=payload)

    def deactivate_vdc(self, vdc_id):
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

        return self.conn.post(
            url='object/vdcs/vdc/{0}/deactivate'.format(vdc_id))
