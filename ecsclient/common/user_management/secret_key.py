import logging

log = logging.getLogger(__name__)


class SecretKey(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get(self, user_id=None, namespace=None):
        """
        Gets all secret keys for the specified user. If the user is not provided,
        it will use authenticated user. If the user belongs to a namespace,
        the namespace must be supplied

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

        :param user_id: Valid user identifier to get the keys from. If not provided,
        the authenticated user will be used instead.
        :param namespace: Namespace for the user if the user belongs to a namespace (optional)
        """
        if user_id:
            msg = "Getting secret keys for user '{}'".format(user_id)
            url = 'object/user-secret-keys/{}'.format(user_id)
            if namespace:
                msg += " in namespace '{}'".format(namespace)
                url += '/{}'.format(namespace)
        else:
            msg = "Getting secret keys for the authenticated user"
            url = 'object/secret-keys'

        log.info(msg)
        return self.conn.get(url)

    def create(self, user_id=None, namespace=None, expiry_time=None, secret_key=None):
        """
        Creates a secret key for the specified user. If the user is not provided,
        it will create the secret key for the authenticated user. If the user
        is provided and belongs to a namespace, the namespace must be supplied.
        You may pass in an expiration time in minutes. During the expiration interval,
        both keys will be accepted for requests. This gives you a grace period where
        you can update applications to use the new key.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        No specific role is required if a user ID is not provided.

        Example JSON result from the API:

        {
            "link": {
                "rel": "self",
                "href":"/object/user-secret-keys/joedeleteme"
            },
            "secret_key": "p3PZyb//Ch6tM0fUsnesYYnGb+6JHV8WHzS5YHjg",
            "key_timestamp": "2014-12-24 02:08:40.181"
        }

        :param user_id: Valid user identifier to create a key for. If not provided,
        the authenticated user will be used instead.
        :param namespace: Namespace for the user if the user belongs to a namespace (optional)
        :param expiry_time: Expiry time in minutes for the previous secret key. Note that nodes may
        cache secret keys for up to two minutes so old keys may not expire immediately.
        Do not provide an expiry time if the user does not have an existing key (optional)
        :param secret_key: Secret key associated with this user. If not provided, system
        will generate one
        """

        payload = dict()

        if expiry_time:
            payload["existing_key_expiry_time_mins"] = expiry_time

        if user_id:
            url = 'object/user-secret-keys/{}'.format(user_id)
            msg = "Creating secret for user '{}'".format(user_id)
            if namespace:
                payload['namespace'] = namespace
            if secret_key:
                payload['secretkey'] = secret_key
        else:
            url = 'object/secret-keys'
            msg = "Creating secret for the authenticated user"
            if secret_key:
                log.warning("Ignoring provided secret key. Cannot set custom secret key for authenticated user")

        log.info(msg)
        return self.conn.post(url, json_payload=payload)

    def delete(self, user_id=None, namespace=None, secret_key=None):
        """
        Deletes all secret keys for the specific user. If the user is not provided,
        it will delete the secret keys for the authenticated user. If the user is
        provided and belongs namespace, the namespace must be supplied.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param user_id: Valid user identifier to get delete the keys from (optional)
        :param namespace: Namespace for the user if the user belongs to a namespace (optional)
        :param secret_key: The secret key to deleted (optional)
        """

        if user_id:
            url = 'object/user-secret-keys/{}/deactivate'.format(user_id)
            msg = "Deleting secret for user '{}'".format(user_id)
        else:
            url = 'object/secret-keys/deactivate'
            msg = "Deleting secret for the authenticated user"

        payload = {}
        if secret_key:
            payload['secret_key'] = secret_key
        if namespace:
            payload['namespace'] = namespace

        log.info(msg)
        return self.conn.post(url, json_payload=payload)
