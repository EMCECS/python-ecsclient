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
        super(TestAuthentication, self).setUp(*args, **kwargs)
        self.client = Client(username='someone',
                             password='password',
                             ecs_endpoint='http://127.0.0.1:4443',
                             token_endpoint='http://127.0.0.1:4443/login')
        self.requests_mock = self.useFixture(fixture.Fixture())

    @mock.patch('ecsclient.baseclient.os.path.isfile')
    def test_get_token_valid_credentials(self, mock_isfile):
        mock_isfile.return_value = False
        self.requests_mock.register_uri('GET', self.LOGIN_URL, headers={'X-SDS-AUTH-TOKEN': 'token'})
        self.assertIsNone(self.client.token)
        self.assertIsNone(self.client._token_request._get_existing_token())

        token = self.client.get_token()

        self.assertEqual(token, 'token')
        self.assertEqual(self.client._token_request._get_existing_token(), 'token')
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.LOGIN_URL)
        self.assertEqual(self.requests_mock.last_request.headers['authorization'],
                         _basic_auth_str('someone', 'password'))

    @mock.patch('ecsclient.baseclient.os.path.isfile')
    def test_get_token_invalid_credentials(self, mock_isfile):
        mock_isfile.return_value = False
        self.requests_mock.register_uri('GET', self.LOGIN_URL, status_code=401, text='body')

        with super(testtools.TestCase, self).assertRaises(ECSClientException) as error:
            self.client.get_token()

        exception = error.exception
        self.assertEqual(exception.message, 'Invalid username or password')
        self.assertEqual(exception.ecs_message, 'body')
        self.assertEqual(exception.http_status_code, 401)
        self.assertIsNone(self.client._token_request._get_existing_token())
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.LOGIN_URL)
        self.assertEqual(self.requests_mock.last_request.headers['authorization'],
                         _basic_auth_str('someone', 'password'))

    @mock.patch('ecsclient.common.token_request.TokenRequest.get_token')
    def test_logout(self, mock_get_token):
        mock_get_token.return_value = 'token'
        self.requests_mock.register_uri('GET', self.LOGOUT_URL, text="{'user': 'someone'}")

        resp = self.client.authentication.logout()

        self.assertEqual(resp, "{'user': 'someone'}")
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.LOGOUT_URL)
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'token')

    @mock.patch('ecsclient.common.token_request.TokenRequest.get_token')
    def test_logout_force(self, mock_get_token):
        mock_get_token.return_value = 'token'
        self.requests_mock.register_uri('GET', self.LOGOUT_URL + '?force=True', text="{'user': 'someone'}")

        resp = self.client.authentication.logout(force=True)

        self.assertEqual(resp, "{'user': 'someone'}")
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, self.LOGOUT_URL + '?force=True')
        self.assertEqual(self.requests_mock.last_request.qs['force'], ['true'])
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'token')
