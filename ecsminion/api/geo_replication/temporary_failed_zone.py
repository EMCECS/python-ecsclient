# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class TemporaryFailedZone(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_all_temp_failed_zones(self):
        """
        Gets all the configured temp failed zones.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'tempfailedzone': [
                {
                    u'remote': None,
                    u'tags': [],
                    u'global': None,
                    u'rgId': u'urn: storageos: ReplicationGroupInfo:
                                c2b0d3c4-c778-4a24-8da5-6a89784c4eeb: global',
                    u'vdc': None,
                    u'inactive': False,
                    u'failedZoneList': []
                },
                {
                    u'remote': None,
                    u'tags': [],
                    u'global': None,
                    u'rgId': u'urn: storageos: ReplicationGroupInfo:
                                4ea1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global',
                    u'vdc': None,
                    u'inactive': False,
                    u'failedZoneList': []
                }
            ]
        }
        """
        log.info("Fetching all Temporary Failed Zones")
        return self.conn.get(url='tempfailedzone/allfailedzones')

    def get_temp_failed_zone(self, replication_group_id):
        """
        Gets all the temp failed zones for the specified replication group
        identifier.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'remote': None,
            u'tags': [],
            u'global': None,
            u'rgId': u'urn: storageos: ReplicationGroupInfo:
                        c2b0d3c4-c778-4a24-8da5-6a89784c4eeb: global',
            u'vdc': None,
            u'inactive': False,
            u'failedZoneList': []
        }

        :param replication_group_id: Replication group id to retrieve details
        """
        log.info("Fetching TFZs for vpool '{0}'".format(replication_group_id))

        return self.conn.get(
            url='tempfailedzone/rgid/{0}'.format(replication_group_id))
