import requests
import testtools
from requests_mock.contrib import fixture

from ecsclient.common.exceptions import ECSClientException


class TestException(testtools.TestCase):
    TEST_URL = 'https://127.0.0.1:4443/foor/bar?param1=value1&param2=value2'

    def setUp(self):
        super(TestException, self).setUp()
        self.requests_mock = self.useFixture(fixture.Fixture())

    def test_is_exception(self):
        self.assertTrue(issubclass(ECSClientException, Exception))

    def test_attrs(self):
        test_kwargs = {
            'ecs_code': '21000',
            'ecs_retryable': True,
            'ecs_description': 'Error description',
            'ecs_details': 'Error details',
            'http_scheme': 'https',
            'http_host': 'localhost',
            'http_port': 4443,
            'http_path': '/path',
            'http_query': 'param1=value1',
            'http_status': 500,
            'http_reason': 'Reason',
            'http_response_content': 'Response content',
            'http_response_headers': [{'x-header-1': 'value1'}]
        }
        exc = ECSClientException('test', **test_kwargs)

        for key, value in test_kwargs.items():
            self.assertIs(True, hasattr(exc, key))
            self.assertEqual(getattr(exc, key), value)

    def test_format(self):
        test_kwargs = {
            'ecs_description': 'Error description',
            'ecs_details': 'Error details',
            'http_scheme': 'https',
            'http_host': 'localhost',
            'http_port': 4443,
            'http_path': '/path',
            'http_query': 'param1=value1',
            'http_status': 500,
            'http_reason': 'Reason',
            'http_response_content': 'Response content'
        }

        for key, value in test_kwargs.items():
            kwargs = {key: value}
            exc = ECSClientException('test', **kwargs)
            self.assertIn(str(value), str(exc))

    def test_from_response(self):
        response_content = '{"code": "1000", "retryable": false, ' \
                           '"description": "Error description", ' \
                           '"details": "Error details"}'
        self.requests_mock.register_uri('POST', self.TEST_URL,
                                        status_code=500,
                                        text=response_content)
        resp = requests.post(self.TEST_URL, data='body')
        exc = ECSClientException.from_response(resp)

        self.assertEqual(exc.ecs_code, '1000')
        self.assertEqual(exc.ecs_retryable, False)
        self.assertEqual(exc.ecs_description, 'Error description')
        self.assertEqual(exc.ecs_details, 'Error details')
        self.assertEqual(exc.http_scheme, 'https')
        self.assertEqual(exc.http_host, '127.0.0.1')
        self.assertEqual(exc.http_port, 4443)
        self.assertEqual(exc.http_path, '/foor/bar')
        self.assertEqual(exc.http_query, 'param1=value1&param2=value2')
        self.assertEqual(exc.http_status, 500)
        self.assertEqual(exc.http_reason, None)
        self.assertEqual(exc.http_response_content, response_content)
