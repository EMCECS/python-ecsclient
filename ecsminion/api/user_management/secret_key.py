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
