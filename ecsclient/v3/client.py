import logging

from ecsclient import baseclient
from ecsclient.v3.configuration import certificate, configuration_properties, licensing, feature, syslog, snmp
from ecsclient.v3.cas import cas

# Initialize logger
from ecsclient.v3.multitenancy import namespace
from ecsclient.v3.other import user_info

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
        self.feature = feature.Feature(self)
        self.syslog = syslog.Syslog(self)
        self.snmp = snmp.Snmp(self)

        # CAS
        self.cas = cas.Cas(self)

        # File System Access

        # Metering

        # Migration

        # Monitoring

        # Dashboard

        # Multi-tenancy
        self.namespace = namespace.Namespace(self)

        # Geo-replication

        # Provisioning

        # Support

        # User Management

        # Other
        self.user_info = user_info.UserInfo(self)
