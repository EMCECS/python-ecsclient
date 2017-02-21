from tests import functional
from tests.functional import schemas


class TestVDC(functional.BaseTestCase):
    def setUp(self):
        super(TestVDC, self).setUp()
        r = self.client.vdc.list()
        self.vdc_1_id = r['vdc'][0]['id']
        self.vdc_1_name = r['vdc'][0]['name']

    def test_vdc_list(self):
        response = self.client.vdc.list()
        self.assertValidSchema(response, schemas.VDCS)

    def test_vdc_get_by_id(self):
        response = self.client.vdc.get(vdc_id=self.vdc_1_id)
        self.assertValidSchema(response, schemas.VDC)
        self.assertEqual(response['id'], self.vdc_1_id)
        self.assertEqual(response['vdcId'], self.vdc_1_id)

    def test_vdc_get_by_name(self):
        response = self.client.vdc.get(name=self.vdc_1_name)
        self.assertValidSchema(response, schemas.VDC)
        self.assertEqual(response['name'], self.vdc_1_name)
        self.assertEqual(response['vdcName'], self.vdc_1_name)

    def test_vdc_get_local(self):
        response = self.client.vdc.get_local()
        self.assertValidSchema(response, schemas.VDC)
        self.assertTrue(response['local'])

    def test_vdc_get_local_secret_key(self):
        response = self.client.vdc.get_local_secret_key()
        self.assertIn('key', response)
        self.assertIsNotNone(response['key'])

    def test_vdc_update(self):
        # response = self.client.vdc.update('vdc1', secret_key='1234567890')
        # FIXME: API always returns 500 error when trying to update a VDC
        self.skipTest('API error')

    def test_vdc_delete(self):
        # response = self.client.vdc.delete('vdc-test-1')
        # FIXME: Won't be able to delete a VDC until the API offers an endpoint to create them
        self.skipTest('API missing create endpoint')

    def test_vdc_create(self):
        # FIXME: API does not offer an endpoint to create a VDC
        self.skipTest('API missing create endpoint')