# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class SecretKeySelfService(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_user_secret_keys(self):
        """
        Gets all configured secret keys for the user account that makes the
        request.

        Required role(s):

        This call has no restrictions.

        Example JSON result from the API:

        {
          "user_secret_keys": {
            "secret_key_1": "",
            "key_timestamp_1": "",
            "key_expiry_timestamp_1": "",
            "secret_key_2": "",
            "key_timestamp_2": "",
            "key_expiry_timestamp_2": ""
          }
        }
        """
        log.info('Getting all secrets for current api user (me)')
        return self.conn.get(url='object/secret-keys')

    def create_new_secret_key(self, key_expiration=2592000):
        """
        Create a secret key for the authenticated user that makes the request.
        When creating new secret key, you may pass in an expiration time in
        minutes for the old key. During the expiration interval, both keys
        will be accepted for requests. This gives you a grace period where you
        can update applications to use the new key.

        Required role(s):

        This call has no restrictions.

        Example JSON result from the API:

        {
            "secret_key":"b2qffCUYCyyKrwoaEKkb1XoYB4m82banbgwUjjxs",
            "key_timestamp":"2015-09-30 20:57:59.149",
            "key_expiry_timestamp":"2015-09-30 20:57:59.149",
            "link":{
                    "rel":"self",
                    "href":"/object/user-secret-keys/root"
                    }
        }

        :param key_expiration: Expiry time/date for the secret
        key in minutes. Note that nodes may cache old keys for up to two
        minutes so the old key may not expire immediately. Defaults to 30 days
        (2592000 seconds)
        """
        payload = {
            "existing_key_expiry_time_mins": key_expiration

        }
        log.info('Creating secret for current api user (me)')
        return self.conn.post(url='object/secret-keys', json_payload=payload)

    def deactivate_user_secret_key(self, secret_key=None):
        """
        Deletes the specified secret key for the authenticated user that makes
        the request.

        Required role(s):

        This call has no restrictions.

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param secret_key: The secret key to deactivate (delete)
        """
        payload = {
            "secret_key": secret_key
        }

        log.info("Deleting secret for current api user (me)")

        return self.conn.post(
            url='object/secret-keys/deactivate', json_payload=payload)
