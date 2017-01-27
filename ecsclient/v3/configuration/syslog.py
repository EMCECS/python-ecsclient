import logging

log = logging.getLogger(__name__)


class Syslog(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_syslog_servers(self):
        """
        Get list of Syslog Server info.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:
        """
        # TODO: Add example JSON response
        log.info("Fetching syslog servers")
        return self.conn.get('vdc/syslog/config')

    def get_syslog_server(self, syslog_id):
        """
        Get Syslog Server info.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:
        {}

        :param syslog_id: Syslog server ID
        """
        # TODO: Add example JSON response
        log.info("Getting syslog server information with ID '{}'".format(syslog_id))
        return self.conn.get('vdc/syslog/config/{}'.format(syslog_id))

    def create_syslog_server(self, server, port, protocol, severity):
        """
        Creates a Syslog server.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:
        {}

        :param server: Fully qualified domain name or IP
        :param port: Syslog port
        :param protocol: Protocol Syslog protocol UDP/TCP
        :param severity: Severity - minimal syslog message severity for this server
        """
        # TODO: Add example JSON response

        payload = {
          "server": server,
          "port": port,
          "protocol": protocol,
          "severity": severity
        }

        log.info("Creating syslog server")
        return self.conn.post('vdc/syslog/config', json_payload=payload)

    def update_syslog_server(self, syslog_id, server, port, protocol, severity):
        """
        Update specified Syslog Server.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param syslog_id: Syslog server ID
        :param server: Fully qualified domain name or IP
        :param port: Syslog port
        :param protocol: Protocol Syslog protocol UDP/TCP
        :param severity: Severity - minimal syslog message severity for this server
        """

        payload = {
            "server": server,
            "port": port,
            "protocol": protocol,
            "severity": severity
        }
        log.info("Updating syslog server with ID '{}'".format(syslog_id))
        return self.conn.put('vdc/syslog/config/{}'.format(syslog_id), json_payload=payload)

    def delete_syslog_server(self, syslog_id):
        """
        Delete specified Syslog Server.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param syslog_id: Syslog server ID
        """
        log.info("Deleting syslog server with ID '{}'".format(syslog_id))
        return self.conn.delete('vdc/syslog/config/{}'.format(syslog_id))
