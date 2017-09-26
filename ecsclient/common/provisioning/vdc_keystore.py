import logging

log = logging.getLogger(__name__)


class VdcKeystore(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get(self):
        """
        Get the certificate chain being used by ECS.

        Required role(s):

        This call has no restrictions.

        Example JSON result from the API:

        {
            "chain": "-----BEGIN CERTIFICATE-----\nMIIDBjCCAe4..."
        }
        """
        log.info("Getting the certificate chain")
        return self.conn.get('vdc/keystore')

    def set(self, private_key, certificate_chain):
        """
        Set the private key and certificate chain being used by ECS.
        WARNING: Note that the certificate will not be updated until ECS is
        restarted. Restarting ECS is out of the scope of this library.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            "chain": "-----BEGIN CERTIFICATE-----\nMIIDBjCCAe4..."
        }

        :param private_key: The private key to be set
        :param certificate_chain: The certificate chain to be set
        """
        payload = {
          "key_and_certificate": {
            "private_key": private_key,
            "certificate_chain": certificate_chain
          }
        }

        log.info("Setting the private key and certificate chain (ECS must be "
                 "restarted for this change to take effect)")
        return self.conn.put('vdc/keystore', json_payload=payload)
