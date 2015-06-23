# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class UserInfo(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def whoami(self):
        """
        Example JSON result from the API:

        {
            u'common_name': u'ecsadmin@internal',
            u'distinguished_name': u'',
            u'namespace': u'',
            u'roles': [
                u'SYSTEM_ADMIN'
            ]
        }
        """

        return self.conn.get('user/whoami')
