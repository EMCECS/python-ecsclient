from ecsclient import schemas
from tests import functional


class TestDashboard(functional.BaseTestCase):

    def __test_get_local_zone_replication_groups(self):
        response = self.client.dashboard.get_local_zone_replication_groups()
        self.assertValidSchema(response, schemas.DASHBOARD_REPLICATION_GROUPS)

    def __test_get_local_zone_nodes(self):
        response = self.client.dashboard.get_local_zone_nodes()
        # TODO: complete the schema to validate the full response
        self.assertValidSchema(response, schemas.DASHBOARD_NODES)

    def test_get_node_disks(self):
        response = self.client.dashboard.get_node_disks()
        print(response)
        # self.assertValidSchema(response, schemas.DASHBOARD_NODES)
