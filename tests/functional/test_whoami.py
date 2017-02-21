from tests import functional
from tests.functional import schemas


class TestWhoami(functional.BaseTestCase):
    def test_whoami(self):
        response = self.client.user_info.whoami()
        self.assertValidSchema(response, schemas.WHOAMI)