import logging

log = logging.getLogger(__name__)


class Feature(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_sse(self):
        """
        Returns the feed for the details of ServerSideEncryption feature

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:
        {}
        """
        # TODO: Add example JSON response
        log.info("Getting Server Side Encryption details")
        return self.conn.get('feature/ServerSideEncryption')
