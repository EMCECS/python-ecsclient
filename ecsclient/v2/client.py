import logging

from ecsclient import baseclient
from ecsclient.v2.cas import cas
from ecsclient.v2.configuration import certificate, configuration_properties, licensing
from ecsclient.v2.geo_replication.replication_group import ReplicationGroup
from ecsclient.v2.geo_replication.temporary_failed_zone import TemporaryFailedZone
from ecsclient.v2.metering.billing import Billing
from ecsclient.v2.monitoring.capacity import Capacity
from ecsclient.v2.monitoring.dashboard import Dashboard
from ecsclient.v2.monitoring.events import Events
from ecsclient.v2.multitenancy import namespace
from ecsclient.v2.other import user_info
from ecsclient.v2.provisioning.base_url import BaseUrl
from ecsclient.v2.provisioning.bucket import Bucket
from ecsclient.v2.provisioning.data_store import DataStore
from ecsclient.v2.provisioning.node import Node
from ecsclient.v2.provisioning import storage_pool, virtual_data_center
from ecsclient.v2.support.call_home import CallHome
from ecsclient.v2.user_management.authentication_provider import AuthenticationProvider
from ecsclient.v2.user_management.secret_key import SecretKey
from ecsclient.v2.user_management.secret_key_self_service import SecretKeySelfService
from ecsclient.v2.user_management.user_management import ManagementUser
from ecsclient.v2.user_management.user_object import ObjectUser

# Initialize logger
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Client(baseclient.Client):
    version = 'v2'

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

        # API -> Billing
        self.billing = Billing(self)

        # API -> Configuration
        self.certificate = certificate.Certificate(self)
        self.configuration_properties = configuration_properties.ConfigurationProperties(self)
        self.licensing = licensing.Licensing(self)

        # API -> CAS
        self.cas = cas.Cas(self)

        # API -> Geo Replication
        self.replication_group = ReplicationGroup(self)
        self.temp_failed_zone = TemporaryFailedZone(self)

        # API -> Monitoring
        self.capacity = Capacity(self)
        self.dashboard = Dashboard(self)
        self.events = Events(self)

        # Multi-tenancy
        self.namespace = namespace.Namespace(self)

        # Provisioning
        self.base_url = BaseUrl(self)
        self.bucket = Bucket(self)
        self.data_store = DataStore(self)
        self.node = Node(self)
        self.storage_pool = storage_pool.StoragePool(self)
        self.vdc = virtual_data_center.VirtualDataCenter(self)

        # API -> Support
        self.call_home = CallHome(self)

        # API -> User Management
        self.authentication_provider = AuthenticationProvider(self)
        self.secret_key = SecretKey(self)
        self.secret_key_self_service = SecretKeySelfService(self)
        self.management_object = ManagementUser(self)
        self.user_object = ObjectUser(self)

        # Other
        self.user_info = user_info.UserInfo(self)
