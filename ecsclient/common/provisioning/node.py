# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class Node(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def list(self):
        """
        Gets a list of the data nodes that are currently configured in the cluster.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'node': [
                {
                    u'ip': u'172.29.3.148',
                    u'version': u'1.2.0.0.60071.ffbe16c',
                    u'rackId': u'gray',
                    u'nodename': u'supr01-r01-01.lax01s1.rspaas-lab.ops.com',
                    u'nodeid': u'171.29.3.140'
                },
                {
                    u'ip': u'172.29.3.149',
                    u'version': u'1.2.0.0.60071.ffbe16c',
                    u'rackId': u'gray',
                    u'nodename': u'supr01-r01-02.lax01s1.rspaas-lab.ops.com',
                    u'nodeid': u'171.29.3.141'
                }
            ]
        }
        """
        log.info('Getting all nodes for cluster')
        return self.conn.get(url='vdc/nodes')
