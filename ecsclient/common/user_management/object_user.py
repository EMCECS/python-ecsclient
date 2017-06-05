import logging


log = logging.getLogger(__name__)


class ObjectUser(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def list(self, namespace=None):
        """
        Gets identifiers for all configured users. If namespace is provided
        then returns all users for the specified namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'blobuser': [
                {
                    u'userid': u'johndoe',
                    u'namespace': u'namespace1'
                },
                {
                    u'userid': u'janedoe',
                    u'namespace': u'namespace1'
                }
            ]
        }

        :param namespace: Namespace for which users should be returned. Optional.
        """
        msg = 'Listing all object users'
        url = 'object/users'

        if namespace:
            url += '/{}'.format(namespace)
            msg += " in namespace '{}'".format(namespace)

        log.info(msg)
        return self.conn.get(url=url)

    def get(self, user_id, namespace=None):
        """
        Gets user details for the specified user.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'locked': False,
            u'namespace': u'namespace1',
            u'name': u'someone',
            u'created': u'ThuMay2105: 43: 27UTC2015'
        }

        :param user_id: Valid user identifier
        :param namespace: Optional when user scope is GLOBAL. Required when
        user scope is NAMESPACE. The namespace to which the user belongs
        """
        msg = "Getting user ID '{}'".format(user_id)
        url = 'object/users/{}/info'.format(user_id)

        if namespace:
            url += '?namespace={}'.format(namespace)
            msg += " in namespace '{}'".format(namespace)

        log.info(msg)
        return self.conn.get(url=url)

    def delete(self, user_id, namespace=None):
        """
        Deletes the specified user and its secret keys.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param user_id: Valid user identifier
        :param namespace: Example: namespace1 (optional)
        """
        payload = {"user": user_id}
        if namespace:
            payload["namespace"] = namespace

        log.info("Deleting user ID '{}'".format(user_id))
        return self.conn.post('object/users/deactivate', json_payload=payload)

    def create(self, user_id, namespace, tags=None):
        """
        Creates a user for a specified namespace. The user must subsequently
        be assigned a secret key in order to access the object store.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            "link": {
              "href": "/object/user-secret-keys/wuser1@sanity.local",
              "rel": "self"
          }
        }

        :param user_id: User to be created
        :param namespace: Namespace identifier to associate with the user
        :param tags: A list of arbitrary tags to assign to the new user. These can
        be used to track additional information about the user and will also
        appear on bucket billing responses for buckets owned by the user
        """

        payload = {
            "user": user_id,
            "namespace": namespace
        }

        if tags:
            payload['tags'] = tags

        log.info('Creating user: {0}'.format(payload))
        return self.conn.post('object/users', json_payload=payload)

    def lock(self, user_id, namespace=None):
        """
        Locks the specified user. If the user belongs to a
        namespace, the namespace must be supplied.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param user_id: User name to be locked
        :param namespace: Namespace for this user (optional)
        """
        return self.__lock(user_id, namespace, True)

    def unlock(self, user_id, namespace=None):
        """
        Unlocks the specified user. If the user belongs to a
        namespace, the namespace must be supplied.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param user_id: User name to be unlocked
        :param namespace: Namespace for this user (optional)
        """
        return self.__lock(user_id, namespace, False)

    def __lock(self, user_id, namespace, lock):
        payload = {
            "user": user_id,
            "isLocked": lock
        }

        if namespace:
            payload["namespace"] = namespace

        verb = "Locking" if lock else "Unlocking"
        log.info("{} user ID {}".format(verb, user_id))
        return self.conn.put(url='object/users/lock', json_payload=payload)

    def get_lock(self, user_id, namespace=None):
        """
        Gets the user lock state for the specified user belonging to the
        specified namespace (if provided).

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'user_name': u'testlogin',
            u'isLocked': False
        }

        :param user_id: User ID for which user lock status should be returned
        :param namespace: Namespace to which user belongs (optional)
        """
        msg = "Getting lock state for user ID '{}'".format(user_id)
        url = 'object/users/lock/{}'.format(user_id)
        if namespace:
            msg += " in namespace '{}'".format(namespace)
            url += '/{}'.format(namespace)

        log.info(msg)
        return self.conn.get(url)
