# coding=utf-8
import logging

log = logging.getLogger(__name__)


class PasswordGroup(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get(self, user_id=None, namespace=None):
        """
        Gets all Swift user groups for a specified user identifier.
        If namespace is provided then returns only groups for the specified namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            "groups_list": [
                "admin"
            ]
        }

        :param user_id: Username for which group names should be returned.
        :param namespace: Namespace limiting returned groups (optional).
        """
        msg = "Getting Swift groups for user '{}'".format(user_id)
        url = 'object/user-password/{}'.format(user_id)

        if namespace:
            url += '/{}'.format(namespace)
            msg += " in namespace '{}'".format(namespace)

        log.info(msg)
        return self.conn.get(url=url)

    def create(self, user_id=None, namespace=None, password=None, groups_list=None):
        """
        Creates password and group for a specific user.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param user_id: Valid user identifier to create a key for. If not provided,
        the authenticated user will be used instead.
        :param namespace: Namespace for the user if the user belongs to a namespace.
        :param groups_list: List of Swift groups with which to associate this user.
        :param password: Swift password associated with this user.
        """

        url = 'object/user-password/{}'.format(user_id)
        msg = "Creating Swift password for user '{}' in namespace '{}'".format(user_id, namespace)

        payload = {'namespace': namespace,
                   'password': password,
                   'groups_list': groups_list}

        log.info(msg)
        return self.conn.put(url, json_payload=payload)

    def update(self, user_id=None, namespace=None, password=None, groups_list=None):
        """
        Updates password and group information for a specific user identifier.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param user_id: Valid user identifier to create a key for. If not provided,
        the authenticated user will be used instead.
        :param namespace: Namespace for the user if the user belongs to a namespace.
        :param groups_list: List of Swift groups with which to associate this user.
        :param password: Swift password associated with this user.
        """

        url = 'object/user-password/{}'.format(user_id)
        msg = "Updating Swift password for user '{}' in namespace '{}'".format(user_id, namespace)

        payload = {'namespace': namespace,
                   'password': password,
                   'groups_list': groups_list}

        log.info(msg)
        return self.conn.post(url, json_payload=payload)

    def delete(self, user_id=None, namespace=None):
        """
        Deletes password group for a specified user.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 204 No Response

        :param user_id: Valid user identifier to get delete the keys from.
        :param namespace: Namespace for the user if the user belongs to a namespace.
        """

        url = 'object/user-password/{}/deactivate'.format(user_id)
        msg = "Deleting Swift password for user '{}' in namespace '{}'".format(user_id, namespace)

        payload = {'namespace': namespace}

        log.info(msg)
        return self.conn.post(url, json_payload=payload)
