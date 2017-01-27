import logging

from ecsclient import baseclient
from ecsclient.v3.configuration import certificate, configuration_properties, licensing, syslog, snmp

# Initialize logger
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Client(baseclient.Client):
    version = 'v3'

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

        # Configuration
        self.certificate = certificate.Certificate(self)
        self.configuration_properties = configuration_properties.ConfigurationProperties(self)
        self.licensing = licensing.Licensing(self)
        self.syslog = syslog.Syslog(self)
        self.snmp = snmp.Snmp(self)

        # CAS

        # File System Access

        # Metering

        # Migration

        # Monitoring

        # Dashboard

        # Multi-tenancy

        # Geo-replication

        # Provisioning

        # Support

        # User Management
