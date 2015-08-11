# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


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
        log.info('Getting my own user info (whoami)')
        return self.conn.get('user/whoami')
