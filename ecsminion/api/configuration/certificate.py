# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


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

        return self.conn.get('object-cert/keystore')

    def put_certificate_chain(self):
        """
        Sets private key and certificate pair. The new certificate and key
        will be rotated into all of the nodes within 1 hour.
        """

        raise NotImplementedError
