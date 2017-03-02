import testtools
from requests_mock.contrib import fixture
from mock import MagicMock
from mock import mock_open
from mock import patch
from six.moves import http_client
from ecsclient.common.token_request import TokenRequest
from ecsclient.common.exceptions import ECSClientException


class TestTokenRequest(testtools.TestCase):

    def setUp(self):
        super(TestTokenRequest, self).setUp()
        self.token_file_contents = '123TOKEN'
        self.response = MagicMock()
        self.session_get = 'ecsclient.common.token_request.requests.Session.get'

        self.token_request = TokenRequest(username='someone',
                                          password='password',
                                          ecs_endpoint='https://127.0.0.1:4443',
                                          token_endpoint='https://127.0.0.1:4443/login',
                                          verify_ssl=False,
                                          token_path='/tmp/ecstoken.tkn',
                                          request_timeout=5.0,
                                          cache_token=True)
        self.requests_mock = self.useFixture(fixture.Fixture())

    def test_should_get_existing_token(self):
        with patch('os.path.isfile', return_value=True),\
            patch('six.moves.builtins.open', mock_open(read_data='123TOKEN'),
                  create=True):
            self.assertEqual(self.token_request._get_existing_token(),
                             self.token_file_contents)

    def test_should_not_get_existing_token(self):
        with patch('os.path.isfile', return_value=False):
            self.assertEqual(self.token_request._get_existing_token(), None)

    def test_get_new_token_should_throw_ecsclientexception_500(self):
        self.requests_mock.register_uri('GET', 'https://127.0.0.1:4443/login',
                                        status_code=http_client.INTERNAL_SERVER_ERROR)

        with super(testtools.TestCase, self).assertRaises(ECSClientException) as error:
            self.token_request.get_new_token()

        exception = error.exception
        self.assertEqual(exception.http_status, http_client.INTERNAL_SERVER_ERROR)

    def test_get_new_token_should_throw_ecsclientexception_401(self):
        self.requests_mock.register_uri('GET', 'https://127.0.0.1:4443/login',
                                        status_code=http_client.UNAUTHORIZED)

        with super(testtools.TestCase, self).assertRaises(ECSClientException) as error:
            self.token_request.get_new_token()

        exception = error.exception
        self.assertEqual(exception.http_status, http_client.UNAUTHORIZED)
