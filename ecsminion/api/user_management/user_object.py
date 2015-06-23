# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class ObjectUser(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_object_users(self, namespace=None):
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

        :param namespace: Example: namespace1


        """
        if namespace:
            return self.conn.get(url='object/users/{0}'.format(namespace))
        else:
            return self.conn.get(url='object/users')

    def get_object_user_info(self, uid, namespace=None):
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

        :param uid: Valid user identifier
        :param namespace: Optional when userscope is GLOBAL. Required when
        userscope is NAMESPACE. The namespace to which the user belongs
        """

        if namespace:
            return self.conn.get(
                url='object/users/{0}/info?namespace={1}'.format(
                    uid, namespace))
        else:
            return self.conn.get(url='object/users/{0}/info'.format(uid))

    def deactivate_object_user(self, uid, namespace=None):
        """
        Deletes the specified user and its secret keys.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param uid: Valid user identifier
        :param namespace: Example: namespace1 (optional)
        """
        if namespace:
            payload = {
                "user": uid,
                "namespace": namespace
            }
        else:
            payload = {
                "user": uid
            }

        return self.conn.post(url='object/users/deactivate',
                              json_payload=payload)

    def add_object_user(self, uid, namespace, tags=None):
        """
        Creates a user for a specified namespace. The user must subsequently
        be assigned a secret key in order to access the object store.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'isLocked': True,
            u'user_name': u'janedoe'
        }

        :param uid: Valid user identifier
        :param namespace: Example: namespace1
        """

        payload = {
            "user": uid,
            "namespace": namespace
        }

        if tags:
            payload['tags'] = tags

        return self.conn.post(url='object/users',
                              json_payload=payload)

    def lock_object_user(self, uid, is_locked=True, namespace=None):
        """
        Locks or unlocks the specified user. If the user belongs to a
        namespace, the namespace must be supplied.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param uid: Valid user identifier
        :param is_locked: Example: True/False (optional)
        :param namespace: Example: namespace1 (optional)
        """
        if namespace:
            payload = {
                "user": uid,
                "namespace": namespace,
                "isLocked": is_locked
            }
        else:
            payload = {
                "user": uid,
                "isLocked": is_locked
            }

        return self.conn.put(url='object/users/lock',
                             json_payload=payload)

    def get_object_user_lock(self, uid, namespace=None):
        """
        Gets the user lock state for the specified user belonging to the
        specified namespace (if provided).

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        TODO: JSON data

        :param uid: Valid user identifier
        :param namespace: Example: namespace1
        """

        if namespace:
            return self.conn.get(
                url='object/users/lock/{0}/{1}'.format(uid, namespace))
        else:
            return self.conn.get(
                url='object/users/lock/{0}'.format(uid))
