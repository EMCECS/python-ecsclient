import logging

from ecsclient import baseclient
from ecsclient.v4.configuration import certificate, configuration_properties, \
    licensing, feature, syslog, snmp
from ecsclient.v4.cas import cas
from ecsclient.v4.metering import billing
from ecsclient.v4.monitoring import capacity, dashboard, events, alerts
from ecsclient.v4.multitenancy import namespace
from ecsclient.v4.multitenancy import tenant
from ecsclient.v4.geo_replication import replication_group, temporary_failed_zone
from ecsclient.v4.provisioning import base_url, bucket, data_store, storage_pool, \
    virtual_data_center, node, vdc_keystore
from ecsclient.v4.user_management import authentication_provider, management_user, \
    object_user, secret_key, password_group
from ecsclient.v4.other import user_info

# Initialize logger
log = logging.getLogger(__name__)


class Client(baseclient.Client):
    version = 'v4'

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

        # File system access
        # TODO: self.nfs = nfs.NFS(self)

        # Metering
        self.billing = billing.Billing(self)

        # Migration
        # TODO: self.transformation = transformation.Transformation(self)

        # Monitoring
        self.capacity = capacity.Capacity(self)
        self.dashboard = dashboard.Dashboard(self)
        self.events = events.Events(self)
        self.alerts = alerts.Alerts(self)

        # Multi-tenancy
        self.namespace = namespace.Namespace(self)
        self.tenant = tenant.Tenant(self)
        # Geo-replication
        self.replication_group = replication_group.ReplicationGroup(self)
        self.temporary_failed_zone = temporary_failed_zone.TemporaryFailedZone(self)

        # Provisioning
        self.base_url = base_url.BaseUrl(self)
        self.bucket = bucket.Bucket(self)
        self.data_store = data_store.DataStore(self)
        self.node = node.Node(self)
        self.storage_pool = storage_pool.StoragePool(self)
        self.vdc = virtual_data_center.VirtualDataCenter(self)
        self.vdc_keystore = vdc_keystore.VdcKeystore(self)

        # Support
        # TODO: self.call_home = call_home.CallHome(self)

        # User Management
        self.authentication_provider = authentication_provider.AuthenticationProvider(self)
        self.password_group = password_group.PasswordGroup(self)
        self.secret_key = secret_key.SecretKey(self)
        self.management_user = management_user.ManagementUser(self)
        self.object_user = object_user.ObjectUser(self)

        # Other
        self.user_info = user_info.UserInfo(self)
