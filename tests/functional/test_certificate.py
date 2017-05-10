from ecsclient import schemas
from tests import functional
from tests.functional import helper


class TestCertificate(functional.BaseTestCase):
    def test_get_certificate(self):
        response = self.client.certificate.get_certificate_chain()
        self.assertValidSchema(response, schemas.CERTIFICATE)

    def test_set_certificate(self):
        # First, set a self-signed certificate
        ip_addresses = ['10.0.0.1']
        response = self.client.certificate.set_certificate_chain(
            selfsigned=True,
            ip_addresses=ip_addresses)
        self.assertValidSchema(response, schemas.CERTIFICATE)

        # Then, provide a private key and a certificate
        private_key = helper.get_sample_private_key()
        certificate = helper.get_sample_certificate()
        response = self.client.certificate.set_certificate_chain(
            private_key=private_key,
            certificate_chain=certificate)
        self.assertValidSchema(response, schemas.CERTIFICATE)
        self.assertSameCertificate(certificate, response['chain'])
