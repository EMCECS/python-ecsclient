from ecsclient import schemas
from tests import functional


class TestAlerts(functional.BaseTestCase):
    def test_alerts_no_params(self):
        response = self.client.alerts.get_alerts()
        # TODO: complete the schema with alert element validation
        self.assertValidSchema(response, schemas.ALERTS)

    def test_alerts_with_params(self):
        self.skipTest("Need to test it with params")
