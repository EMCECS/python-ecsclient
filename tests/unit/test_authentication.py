import logging
import testtools
from mock import mock
from requests.auth import _basic_auth_str
from requests_mock.contrib import fixture

from ecsclient.baseclient import Client
from ecsclient.common.exceptions import ECSClientException


class TestAuthentication(testtools.TestCase):
    LOGIN_URL = 'http://127.0.0.1:4443/login'
    LOGOUT_URL = 'http://127.0.0.1:4443/logout'

    def setUp(self, *args, **kwargs):
        # logging.basicConfig(level=logging.DEBUG)
        super(TestAuthentication, self).setUp(*args, **kwargs)
        self.client = Client(username='someone',
                             password='password',
                             ecs_endpoint='http://127.0.0.1:4443',
                             token_endpoint='http://127.0.0.1:4443/login')
        self.requests_mock = self.useFixture(fixture.Fixture())

    def test_get_token_valid_credentials(self):
        self.requests_mock.register_uri('GET', self.LOGIN_URL, headers={'X-SDS-AUTH-TOKEN': 'FAKE-TOKEN-123'})
        self.assertIsNone(self.client.token)

        token = self.client.get_token()

        self.assertEqual(token, 'FAKE-TOKEN-123')
        self.assertEqual(self.client._token_request.token, 'FAKE-TOKEN-123')
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.LOGIN_URL)
        self.assertEqual(self.requests_mock.last_request.headers['authorization'],
                         _basic_auth_str('someone', 'password'))

    def test_get_token_invalid_credentials(self):
        self.requests_mock.register_uri('GET', self.LOGIN_URL, status_code=401, text='body')

        with super(testtools.TestCase, self).assertRaises(ECSClientException) as error:
            self.client.get_token()

        exception = error.exception
        self.assertIsNone(self.client._token_request.token)
        self.assertEqual(exception.message, 'Invalid username or password')
        self.assertEqual(exception.http_response_content, 'body')
        self.assertEqual(exception.http_status, 401)
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.LOGIN_URL)
        self.assertEqual(self.requests_mock.last_request.headers['authorization'],
                         _basic_auth_str('someone', 'password'))

    @mock.patch('ecsclient.baseclient.os.remove')
    @mock.patch('ecsclient.baseclient.os.path.isfile')
    def test_logout(self, mock_isfile, mock_remove):
        self.client.token = 'FAKE-TOKEN-123'
        self.client._token_request.token = 'FAKE-TOKEN-123'
        self.requests_mock.register_uri('GET', self.LOGOUT_URL, text="{'user': 'someone'}")
        mock_isfile.return_value = True
        mock_remove.return_value = True

        resp = self.client.authentication.logout()

        self.assertEqual(resp, "{'user': 'someone'}")
        self.assertIsNone(self.client.token)
        self.assertIsNone(self.client._token_request.token)
        mock_isfile.assert_called_with('/tmp/ecsclient.tkn')
        mock_remove.assert_called_with('/tmp/ecsclient.tkn')
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.LOGOUT_URL)
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'FAKE-TOKEN-123')

    @mock.patch('ecsclient.baseclient.os.remove')
    @mock.patch('ecsclient.baseclient.os.path.isfile')
    def test_logout_force(self, mock_isfile, mock_remove):
        self.client.token = 'FAKE-TOKEN-123'
        self.client._token_request.token = 'FAKE-TOKEN-123'
        self.requests_mock.register_uri('GET', self.LOGOUT_URL + '?force=True', text="{'user': 'someone'}")
        mock_isfile.return_value = True
        mock_remove.return_value = True

        resp = self.client.authentication.logout(force=True)

        self.assertEqual(resp, "{'user': 'someone'}")
        self.assertIsNone(self.client.token)
        self.assertIsNone(self.client._token_request.token)
        mock_isfile.assert_called_with('/tmp/ecsclient.tkn')
        mock_remove.assert_called_with('/tmp/ecsclient.tkn')
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.LOGOUT_URL + '?force=True')
        self.assertEqual(self.requests_mock.last_request.qs['force'], ['true'])
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'FAKE-TOKEN-123')

    def test_logout_when_logged_out(self):
        self.client._token_request.token = 'FAKE-TOKEN-123'
        self.client._token_request.cache_token = False
        self.requests_mock.register_uri('GET', self.LOGOUT_URL, text="{'user': 'someone'}")
        self.requests_mock.register_uri('GET', 'http://127.0.0.1:4443/user/whoami')

        resp = self.client.authentication.logout()

        self.assertEqual(resp, "{'user': 'someone'}")

        resp2 = self.client.authentication.logout()

        self.assertIsNone(resp2)

    def test_logout_and_reconnect(self):
        self.client.token = 'FAKE-TOKEN-123'
        self.client._token_request.token = 'FAKE-TOKEN-123'
        self.client._token_request.cache_token = False
        self.requests_mock.register_uri('GET', self.LOGOUT_URL, text="{'user': 'someone'}")

        self.client.authentication.logout()

        self.assertIsNone(self.client.token)
        self.assertIsNone(self.client._token_request.token)

        self.requests_mock.register_uri('GET', self.LOGIN_URL, headers={'X-SDS-AUTH-TOKEN': 'NEW-TOKEN-123'})

        self.client.get('login')

        self.assertEqual(self.client._token_request.token, 'NEW-TOKEN-123')


