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
                    u'name': u'viva01',
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
                    u'vdcId': u'urn: storageos: VirtualDataCenterData: a9faea85-d377-4a42-b5f1-fa15829f0c33',
                    u'vdc': None,
                    u'inactive': False,
                    u'link': {
                        u'href': u'/object/vdcs/vdc/tiva01',
                        u'rel': u'self'
                    },
                    u'secretKeys': u'55fmIFBniRuCBVx327Av',
                    u'vdcName': u'tiva01',
                    u'local': True,
                    u'id': u'urn: storageos: VirtualDataCenterData: a9faea85-d377-4a42-b5f1-fa15829f0c33',
                    u'permanentlyFailed': False
                },
                {
                    u'remote': None,
                    u'name': u'viva02',
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
                    u'vdcId': u'urn: storageos: VirtualDataCenterData: 7d7d2ed5-e253-4be9-b8bb-5ff5b2697e6f',
                    u'vdc': None,
                    u'inactive': False,
                    u'link': {
                        u'href': u'/object/vdcs/vdc/tiva02',
                        u'rel': u'self'
                    },
                    u'secretKeys': u'99TilKh9aTwt9fLbCiKd',
                    u'vdcName': u'tiva02',
                    u'local': False,
                    u'id': u'urn: storageos: VirtualDataCenterData: 7d7d2ed5-e253-4be9-b8bb-5ff5b2697e6f',
                    u'permanentlyFailed': False
                }
            ]
        }
        """

        return self.conn.get(
            url='object/vdcs/vdc/list')