# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class Licensing(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_license(self):
        """
        Gets the currently configured licenses.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'license_feature': [
                {
                    u'notice': u'ACTIVATEDTOLicenseSiteNumber:
                                PTA06JUN20131086059',
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
                    u'notice': u'ACTIVATEDTOLicenseSiteNumber:
                                PTA06JUN20131086059',
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
        log.info("Retrieving license")
        return self.conn.get('license')

    def add_license(self, license):
        """
        Adds specified license.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            'license': {
                u'license_feature': [
                    {
                        u'issued_date': u'01/10/2014',
                        u'expired_ind': False,
                        u'issuer': u'EMC',
                        u'license_id_indicator': u'U',
                        u'licensed_ind': True,
                        u'model': u'ViPR_ECS',
                        u'notice': u'ACTIVATED TO License Site Number: XYZ789',
                        u'product': u'PXTYD1DZK59Y4C',
                        u'serial': u'PXTYD1DZK59Y4C',
                        u'site_id': u'UNKNOWN',
                        u'storage_capacity': u'TB',
                        u'trial_license_ind': False,
                        u'version': u'2.0'
                    }
                ],
                u'license_text': u'LicenseText'
            }
        }
        """
        log.info("Adding new license: {0}".format(license))
        return self.conn.post(url='license', json_payload=license)
