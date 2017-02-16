import logging

from ecsclient import baseclient
from ecsclient.v3.configuration import certificate, configuration_properties, licensing, feature, syslog, snmp
from ecsclient.v3.cas import cas
from ecsclient.v3.multitenancy import namespace
from ecsclient.v3.other import user_info
from ecsclient.v3.geo_replication import replication_group
from ecsclient.v3.provisioning import storage_pool, virtual_data_center

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
        self.replication_group = replication_group.ReplicationGroup(self)

        # Provisioning
        self.storage_pool = storage_pool.StoragePool(self)
        self.vdc = virtual_data_center.VirtualDataCenter(self)

        # Support

        # User Management

        # Other
        self.user_info = user_info.UserInfo(self)
