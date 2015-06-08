# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class Licensing:

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_license(self, category='ALL'):
        """
        Gets the currently configured licenses.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'license_feature': [
                {
                    u'notice': u'ACTIVATEDTOLicenseSiteNumber: PTA06JUN20131086059',
                    u'trial_license_ind': False,
                    u'expired_ind': False,
                    u'licensed_ind': True,
                    u'site_id': u'UNKNOWN',
                    u'product': u'PXTYD1DZK59Y4C',
                    u'issued_date': u'01/10/2014',
                    u'version': u'2.0',
                    u'storage_capacity': u'TB',
                    u'license_id_indicator': u'U',
                    u'model': u'ViPR_Block',
                    u'serial': u'PRTYD1DZK59X9A',
                    u'issuer': u'EMC'
                },
                {
                    u'notice': u'ACTIVATEDTOLicenseSiteNumber: PTA06JUN20131086059',
                    u'trial_license_ind': False,
                    u'expired_ind': False,
                    u'licensed_ind': True,
                    u'site_id': u'UNKNOWN',
                    u'product': u'PXTYD1DZK59Y4C',
                    u'issued_date': u'01/10/2014',
                    u'version': u'2.0',
                    u'storage_capacity': u'TB',
                    u'license_id_indicator': u'U',
                    u'model': u'ViPR_Commodity',
                    u'serial': u'PRTYD1DZK59X9A',
                    u'issuer': u'EMC'
                }
            ],
            u'license_text': u'LONG-LONG--TEXT'
        }
        """
        return self.conn.get('license')
