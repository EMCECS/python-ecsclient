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

    def add_license(self, license_text):
        """
        Adds specified license.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param license_text: License text to be added
        """
        payload = {
            "license_text": license_text
        }
        log.info("Adding a new license")
        return self.conn.post('license.json', json_payload=payload)
