import logging

log = logging.getLogger(__name__)


class Certificate(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_certificate_chain(self):
        """
        Gets the certificate chain currently used. The data returned will
        contain all of the certificates in the current certificate chain
        encoded in PEM format.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            u'chain': u'-----BEGINCERTIFICATE-----\nMIIEnTCCA4WgAwI-
            REALLY-LONG-CERT\r\n-----ENDCERTIFICATE-----'
        }
        """
        log.info("Fetching certificate chain")
        return self.conn.get('object-cert/keystore')

    def set_certificate_chain(self, selfsigned=False, ip_addresses=None, private_key=None, certificate_chain=None):
        """
        Sets private key and certificate pair. The new certificate and key
        will be rotated into all of the nodes within 1 hour.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API

        {
            'chain': '-----BEGINCERTIFICATE-----\nMIIEnTCCA4WgAwI-
            REALLY-LONG-CERT\r\n-----ENDCERTIFICATE-----'
        }

        :param selfsigned: Set true if the you want the system to generate a new self-signed certificate,
        false otherwise
        :param ip_addresses: List of IP addresses. The IP addresses are taken into account only if selfsigned
        is set to true. i.e, User wants the system to generate a new self-signed certificate
        :param private_key: The private key used to sign the certificate in PEM format
        :param certificate_chain: New certificate for the nodes in PEM format. For certificates signed by an
        intermediate CA (most are), the intermediate certificate(s) should be concatenated to the text string,
        also in PEM format.
        """
        payload = {
            "system_selfsigned": selfsigned
        }
        if selfsigned:
            payload["ip_addresses"] = ip_addresses
        else:
            payload["key_and_certificate"] = {
                "private_key": private_key,
                "certificate_chain": certificate_chain
            }
        log.info("Setting certificate chain")
        return self.conn.put('object-cert/keystore', json_payload=payload)
