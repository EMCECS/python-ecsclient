import json

import testtools
from requests_mock.contrib import fixture
from six import string_types

from ecsclient.client import Client


class TestHttp(testtools.TestCase):

    TEST_URL = 'http://127.0.0.1:4443/hi'

    def __init__(self, *args, **kwargs):
        super(TestHttp, self).__init__(*args, **kwargs)
        self.client = Client('3',
                             username='user',
                             password='password',
                             token='token',
                             ecs_endpoint='http://127.0.0.1:4443',
                             token_endpoint='http://127.0.0.1:4443/login')

    def setUp(self):
        super(TestHttp, self).setUp()
        self.requests_mock = self.useFixture(fixture.Fixture())

    def test_get_request_plaintext_resp(self):
        self.requests_mock.register_uri('GET', self.TEST_URL, text='resp')

        body = self.client.get('hi', params={'key1': 'value1'})

        self.assertIsInstance(body, string_types)
        self.assertEqual('resp', body)
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.TEST_URL + '?key1=value1')
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'token')

    def test_get_request_json_resp(self):
        self.requests_mock.register_uri('GET', self.TEST_URL, text='{"key2": "value2"}')

        body = self.client.get('hi', params={'key1': 'value1'})

        self.assertIsInstance(body, dict)
        self.assertEqual(body['key2'], "value2")
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.TEST_URL + '?key1=value1')
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'token')

    def test_post_request(self):
        self.requests_mock.register_uri('POST', self.TEST_URL, text=None)

        payload = {'key1': 'value1', 'key2': 'value2'}
        self.client.post('hi', json_payload=payload)

        self.assertEqual(self.requests_mock.last_request.method, 'POST')
        self.assertEqual(json.loads(self.requests_mock.last_request.text), payload)
        self.assertEqual(self.requests_mock.last_request.url, self.TEST_URL)
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'token')

    def test_put_request(self):
        self.requests_mock.register_uri('PUT', self.TEST_URL, text=None)

        payload = {'key1': 'value1', 'key2': 'value2'}
        self.client.put('hi', json_payload=payload)

        self.assertEqual(self.requests_mock.last_request.method, 'PUT')
        self.assertEqual(json.loads(self.requests_mock.last_request.text), payload)
        self.assertEqual(self.requests_mock.last_request.url, self.TEST_URL)
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'token')

    def test_delete_request(self):
        self.requests_mock.register_uri('DELETE', self.TEST_URL, text=None)

        self.client.delete('hi')

        self.assertEqual(self.requests_mock.last_request.method, 'DELETE')
        self.assertEqual(self.requests_mock.last_request.url, self.TEST_URL)
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'token')