import logging

log = logging.getLogger(__name__)


class Alerts(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_alerts(self, namespace=None, start_time=None, end_time=None, marker=None, limit=None,
                   severity=None, type=None, acknowledged=None):
        """
        Gets the list of alerts with optional filters

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            ...
        }

        :param namespace: Namespace for which alerts should be listed
        :param start_time: Start time for listing alerts
        :param end_time: End time for listing alerts
        :param marker: Reference to last alert returned
        :param limit: Number of alerts requested in current fetch
        :param severity: Severity of alerts to be listed
        :param type: Type of alerts to be listed
        :param acknowledged: Boolean to filter by acknowledgement
        """

        filters = {}
        if namespace:
            filters['namespace'] = namespace
        if start_time:
            filters['start_time'] = start_time
        if end_time:
            filters['end_time'] = end_time
        if marker:
            filters['marker'] = marker
        if limit:
            filters['limit'] = limit
        if severity:
            filters['severity'] = severity
        if type:
            filters['type'] = type
        if acknowledged:
            filters['acknowledged'] = acknowledged

        log.info("Getting alerts with filters: %s", (filters,))
        return self.conn.get(url='vdc/alerts', params=filters)
