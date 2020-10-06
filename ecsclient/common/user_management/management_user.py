import logging

log = logging.getLogger(__name__)


class ManagementUser(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def list(self):
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
                    u'isSecurityAdmin': False,
                    u'userId': u'someone@internal',
                    u'isSystemAdmin': True
                },
                {
                    u'isSystemMonitor': False,
                    u'isSecurityAdmin': False,
                    u'userId': u'root',
                    u'isSystemAdmin': True
                }
            ]
        }
        """
        log.info('Listing all local management users')
        return self.conn.get(url='vdc/users')

    def get(self, user_id):
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
            u'isSecurityAdmin': True
        }

        :param user_id: User identifier for which local user information needs to
        be retrieved
        """
        log.info("Getting local management user '{}'".format(user_id))
        return self.conn.get(url='vdc/users/{}'.format(user_id))

    def delete(self, user_id):
        """
        Deletes local management user information for the specified user
        identifier.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param user_id: User identifier for which local user information needs to
        be deleted.
        """
        log.info("Deleting local management user '{}'".format(user_id))
        return self.conn.post(url='vdc/users/{}/deactivate'.format(user_id))

    def create(self, user_id, password, is_system_admin=False,
               is_system_monitor=False, is_security_admin=False):
        """
        Creates local users for the VDC. These users can be assigned to
        VDC-wide management roles and are not associated with a namespace.
        User account can be assigned to the System Admin role by setting the
        isSystemAdmin flag in the request payload.

        Required role(s):

        SYSTEM_ADMIN

        :param user_id: Management user id, ex: sampleuser
        :param password: Password for the management user
        :param is_system_admin: If set to True, assigns the management user to
        the System Admin role. Default: False
        :param is_system_monitor: If set to True, assigns the management user
        to the System Monitor role. Default: False
        :param is_security_admin: If set to True, assigns the management user
        to the Security Admin role. Default: False
        """
        payload = {
            "userId": user_id,
            "password": password,
            "isSystemAdmin": is_system_admin,
            "isSystemMonitor": is_system_monitor,
            "isSecurityAdmin": is_security_admin
        }

        log.info("Creating local management user '{}'".format(user_id))
        return self.conn.post(url='vdc/users', json_payload=payload)

    def update(self, user_id, password, is_system_admin=False,
               is_system_monitor=False, is_security_admin=False):
        """
        Updates user details for the specified local management user.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param user_id: User identifier for which local user information needs to
        be updated.
        :param password: Password for the management user
        :param is_system_admin: If set to True, assigns the management user to
        the System Admin role. Default: False
        :param is_system_monitor: If set to True, assigns the management user
        to the System Monitor role. Default: False
        :param is_security_admin: If set to True, assigns the management user
        to the Security Admin role. Default: False
        """
        payload = {
            "password": password,
            "isSystemAdmin": is_system_admin,
            "isSystemMonitor": is_system_monitor,
            "isSecurityAdmin": is_security_admin
        }

        log.info("Updating local management user '{}'".format(user_id))

        return self.conn.put(
            url='vdc/users/{}'.format(user_id), json_payload=payload)
