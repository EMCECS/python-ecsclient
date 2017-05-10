import time

from ecsclient import schemas
from tests import functional


class TestVDC(functional.BaseTestCase):
    def setUp(self):
        super(TestVDC, self).setUp()
        r = self.client.vdc.get_local()
        self.vdc_1_id = r['id']
        self.vdc_1_name = r['name']
        self.vdc_1_endpoint = r['interVdcEndPoints']

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
        vdc_name = 'vdc-%d' % time.time()
        secret_key = '%d' % time.time()
        self.client.vdc.update(self.vdc_1_name,
                               new_name=vdc_name,
                               secret_key=secret_key,
                               inter_vdc_endpoints=self.vdc_1_endpoint,
                               inter_vdc_cmd_endpoints=self.vdc_1_endpoint,
                               management_endpoints=self.vdc_1_endpoint
                               )

        r = self.client.vdc.get(vdc_id=self.vdc_1_id)
        self.assertEqual(r['name'], vdc_name)
        self.assertEqual(r['vdcName'], vdc_name)
        self.assertEqual(r['secretKeys'], secret_key)

    def test_vdc_delete(self):
        self.skipTest('Cannot create a scenario to delete a VDC')
