from ecsclient import schemas
from tests import functional
from tests.functional import helper


class TestVdcKeystore(functional.BaseTestCase):

    def test_vdc_keystore_get(self):
        response = self.client.vdc_keystore.get()
        self.assertValidSchema(response, schemas.VDC_KEYSTORE)

    def test_vdc_keystore_set(self):
        private_key = helper.get_sample_private_key()
        certificate = helper.get_sample_certificate()
        response = self.client.vdc_keystore.set(private_key, certificate)
        self.assertValidSchema(response, schemas.VDC_KEYSTORE)
        # Can't validate the certificate and private key at this point
        # because it does not take effect until the ECS is manually restarted
        # self.assertSameCertificate(certificate, response['chain'])
