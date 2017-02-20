from tests import functional
from tests.functional import schemas


class TestLicense(functional.BaseTestCase):
    def test_get_license(self):
        response = self.client.licensing.get_license()
        self.assertValidSchema(response, schemas.LICENSE)

    def test_add_license(self):
        license = {
            "license_text": self.license_text
        }
        response = self.client.licensing.add_license(license)
        print(response)