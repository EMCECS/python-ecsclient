# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class Events(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_audit_events(self, start_time, end_time, namespace, limit=10,
                         marker=None):
        """
        Gets audit events for the specified namespace identifier and interval.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'MaxEvents': 2,
            u'NextMarker': u'kNDVkLTRkYzYtOWUxNy03MGFkYzAzMWUxNDQ=',
            u'auditevent': [
                {
                    u'serviceType': u'Bucket',
                    u'description': u'BucketCreated',
                    u'eventType': u'Created',
                    u'userId': u'user1',
                    u'timestamp': u'2015-06-08T01: 30',
                    u'namespace': u'namespace1',
                    u'resourceId': u'namespace1.ecstest-2a925333-5f91-43d0-b1',
                    u'id': u'urn: storageos: Event: 29ffd597-7c64-41ef-bc5c-e2'
                },
                {
                    u'serviceType': u'Bucket',
                    u'description': u'BucketCreated',
                    u'eventType': u'Created',
                    u'userId': u'someone1',
                    u'timestamp': u'2015-06-08T01: 49',
                    u'namespace': u'namespace1',
                    u'resourceId': u'namespace1.ecstest-18880408-64ed-4380-80',
                    u'id': u'urn: storageos: Event: 1ee5c8c2-be67-478a-86ac'
                }
            ]
        }

        Time format is: yyyy-MM-dd'T'HH:mm
        Example: 2015-01-25T04:05

        :param start_time: Start time for the interval to retrieve audit events
        :param end_time: End time for the interval to retrieve audit events
        :param namespace: Namespace identifier for which audit events needs to
        be retrieved.
        :param limit: Number of audit events requested in current fetch.
        :param marker: Reference of last audit event returned
        """
        log.info("Getting audit events for namespace '{0}'".format(namespace))

        params = {
            'start_time': start_time,
            'end_time': end_time,
            'namespace': namespace,
            'limit': limit
        }

        if marker:
            params['marker'] = marker

        return self.conn.get(url='vdc/events', params=params)
