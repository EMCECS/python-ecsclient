# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class ManagementUser(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def create_local_user_info(self, uid, password, is_system_admin=False,
                               is_system_monitor=False):
        """
        Creates local users for the VDC. These users can be assigned to
        VDC-wide management roles and are not associated with a namespace.
        User account can be assigned to the System Admin role by setting the
        isSystemAdmin flag in the request payload.

        Required role(s):

        SYSTEM_ADMIN

        :param uid: Management user id, ex: sampleuser
        :param password: Password for the management user
        :param is_system_admin: If set to true, assigns the management user to
        the System Admin role
        :param is_system_monitor: If set to true, assigns the management user
        to the System Monitor role
        """
        payload = {
            "user": uid,
            "password": password,
            "is_system_admin": is_system_admin,
            "is_system_monitor": is_system_monitor
        }

        return self.conn.post(url='vdc/users', json_payload=payload)

    def delete_local_user_info(self, uid):
        """
        Deletes local management user information for the specified user
        identifier.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param uid: User identifier for which local user information needs to
        be deleted.
        """

        return self.conn.post(url='vdc/users/{0}/deactivate'.format(uid))

    def modify_local_user_info(self, uid, password, is_system_admin=False,
                               is_system_monitor=False):
        """
        Updates user details for the specified local management user.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param uid: User identifier for which local user information needs to
        be updated.
        :param password: Password for the management user
        :param is_system_admin: Assigns or removes management user to /from
        System Admin role.
        :param is_system_monitor: Assigns or removes management user to /from
        System Monitor role.
        """
        payload = {
            "user": uid,
            "password": password,
            "is_system_admin": is_system_admin,
            "is_system_monitor": is_system_monitor
        }

        return self.conn.put(
            url='vdc/users/{0}'.format(uid), json_payload=payload)

    def get_local_user_info(self, uid):
        """
        Gets details for the specified local management user.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'isSystemMonitor': False,
            u'userId': u'admin',
            u'isSystemAdmin': True
        }

        :param uid: User identifier for which local user information needs to
        be retrieved
        """

        return self.conn.get(url='vdc/users/{0}'.format(uid))

    def get_local_management_users(self):
        """
        Gets all configured local management users.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'mgmt_user_info': [
                {
                    u'isSystemMonitor': False,
                    u'userId': u'someone@internal',
                    u'isSystemAdmin': True
                },
                {
                    u'isSystemMonitor': False,
                    u'userId': u'root',
                    u'isSystemAdmin': True
                }
            ]
        }
        """

        return self.conn.get(url='vdc/users')
