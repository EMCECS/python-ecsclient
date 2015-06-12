# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class SecretKey:

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_user_secret_keys(self, uid, namespace=None):
        """
        Gets all secret keys for the specified user.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'key_timestamp_2': u'2015-05-2105: 43: 33.281',
            u'key_timestamp_1': u'2015-05-2105: 43: 30.872',
            u'key_expiry_timestamp_2': u'',
            u'key_expiry_timestamp_1': u'',
            u'secret_key_1': u'3tW4A5G7QaAGVtsGLVL8uDy73S2A6LrvkPTDNdrk',
            u'secret_key_2': u'v5LjgoEM9lqHIo+qa7pIhGjrecc/Wv+WVw7kO4oQ',
            u'link': {
                u'href': u'/object/secret-keys',
                u'rel': u'self'
            }
        }

        :param uid: Valid user identifier to get the keys from
        :param namespace: The namespace
        """

        if namespace:
            return self.conn.get(
                url='object/user-secret-keys/{0}/{1}'.format(uid, namespace))
        else:
            return self.conn.get(url='object/user-secret-keys/{0}'.format(uid))

    def create_new_secret_key(self, uid, namespace=None,
                              key_expiration=2592000, secret_key=None):
        """
        Creates a secret key for the specified user. If the user belongs to a
        namespace, the namespace must be supplied. When creating a new secret
        key, you may pass in an expiration time in minutes for the old key.
        During the expiration interval, both keys will be accepted for
        requests. This gives you a grace period where you can update
        applications to use the new key.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            "link": {
                "rel": "self",
                "href":"/object/user-secret-keys/joedeleteme"
            },
            "secret_key": "p3PZyb//Ch6tM0fUsnesYYnGb+6JHV8WHzS5YHjg",
            "key_timestamp": "2014-12-24 02:08:40.181"
        }

        :param uid: Valid user identifier to create a key for
        :param namespace: The namespace
        :param key_expiration: Defaults to 30 days (2592000 seconds)
        :param secret_key: Manually specify the new secret key
        """
        payload = {
            "existing_key_expiry_time_mins": key_expiration,
            "namespace": namespace
        }

        if secret_key:
            payload['secretkey'] = secret_key

        return self.conn.post(url='object/user-secret-keys/{0}'.format(uid),
                              json_payload=payload)

    def deactivate_user_secret_key(self, uid, namespace=None,
                                   secret_key=None):
        """
        Deletes all secret keys for the specific user. If the user belongs
        namespace, the namespace must be supplied.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param uid: Valid user identifier to get delete the keys from
        :param namespace: The namespace
        :param secret_key: The secret key to deactivate
        """
        payload = {
            "secret_key": secret_key,
            "namespace": namespace
        }

        return self.conn.post(
            url='object/user-secret-keys/{0}/deactivate'.format(uid),
            json_payload=payload)
