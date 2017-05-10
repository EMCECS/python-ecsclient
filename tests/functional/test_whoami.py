from ecsclient import schemas
from tests import functional


class TestWhoami(functional.BaseTestCase):
    def test_whoami(self):
        response = self.client.user_info.whoami()
        self.assertValidSchema(response, schemas.WHOAMI)
