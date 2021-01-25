import logging

log = logging.getLogger(__name__)


class Snmp(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_snmp_agent(self):
        """
        Get SNMP Agent configuration including targets.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:
        """
        # TODO: Add example JSON response
        log.info("Fetching SNMP Agent configuration")
        return self.conn.get('vdc/snmp/config')

    def update_snmp_agent(self, engine_id):
        """
        Sets SNMP agent configuration

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param engine_id: Fully qualified domain name or IP and port
        """
        payload = {
            "engineID": engine_id
        }
        log.info("Setting SNMP agent configuration with Engine ID '{}'".format(engine_id))
        return self.conn.put('vdc/snmp/config', json_payload=payload)

    def get_snmp_target(self, target_id):
        """
        Get SNMP target info.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:
        {}

        :param target_id: SNMP target ID
        """
        # TODO: Add example JSON response
        log.info("Getting SNMP target information with ID '{}'".format(target_id))
        return self.conn.get('vdc/snmp/config/target/{}'.format(target_id))

    def create_snmp_target(self, server, port, version, community, username, auth_protocol,
                           auth_passphrase, privacy_protocol, privacy_passphrase):
        """
        Adds SNMP Target.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:
        {}

        Expect: HTTP/1.1 200 OK

        :param server: Fully qualified domain name or IP
        :param port: SNMP port
        :param version: SNMP version ('V2' or 'V3')
        :param community: Community name (only needed when version is 'V2')
        :param username: Username for authentication
        :param auth_protocol: Authentication protocol ('MD5' or 'SHA')
        :param auth_passphrase: Authentication passphrase
        :param privacy_protocol: Encryption protocol ('DES' or 'AES')
        :param privacy_passphrase: Encryption passphrase
        """
        # TODO: Add example JSON response

        payload = {
            "server": server,
            "port": port,
            "version": version,
            "community": community,
            "user_security_model": {
                "username": username,
                "authentication": {
                    "protocol": auth_protocol,
                    "passphrase": auth_passphrase
                },
                "privacy": {
                    "protocol": privacy_protocol,
                    "passphrase": privacy_passphrase
                }
            }
        }

        log.info("Creating SNMP target")
        return self.conn.post('vdc/snmp/config/target', json_payload=payload)

    def update_snmp_target(self, target_id, server, port, version, community, username,
                           auth_protocol, auth_passphrase, privacy_protocol,
                           privacy_passphrase):
        """
        Adds SNMP Target.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param server: Fully qualified domain name or IP
        :param port: SNMP port
        :param version: SNMP version ('V2' or 'V3')
        :param community: Community name (only needed when version is 'V2')
        :param username: Username for authentication
        :param auth_protocol: Authentication protocol ('MD5' or 'SHA')
        :param auth_passphrase: Authentication passphrase
        :param privacy_protocol: Encryption protocol ('DES' or 'AES')
        :param privacy_passphrase: Encryption passphrase
        """

        payload = {
            "server": server,
            "port": port,
            "version": version,
            "community": community,
            "user_security_model": {
                "username": username,
                "authentication": {
                    "protocol": auth_protocol,
                    "passphrase": auth_passphrase
                },
                "privacy": {
                    "protocol": privacy_protocol,
                    "passphrase": privacy_passphrase
                }
            }
        }

        log.info("Updating SNMP target with ID '{}'".format(target_id))
        return self.conn.put('vdc/snmp/config/target/{}'.format(target_id),
                             json_payload=payload)

    def delete_snmp_target(self, target_id):
        """
        Delete specified SNMP target.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param target_id: SNMP target ID
        """
        log.info("Deleting SNMP target with ID '{}'".format(target_id))
        return self.conn.delete('vdc/snmp/config/target/{}'.format(target_id))
