import unittest
from mock import MagicMock
from mock import mock_open
from mock import patch
from six.moves import http_client
from ecsclient.common.token_request import TokenRequest
from ecsclient.common.exceptions import ECSClientException


class TestTokenRequest(unittest.TestCase):

    def setUp(self):
        self.token_file_contents = '123TOKEN'
        self.response = MagicMock()
        self.session_get = 'ecsclient.common.token_request.requests.Session.get'

        self.token_request = TokenRequest(username='someone',
                                          password='password',
                                          ecs_endpoint='https://localhost',
                                          token_endpoint='https://localhost',
                                          verify_ssl=False,
                                          token_path='/tmp/ecstoken.tkn',
                                          request_timeout=5.0,
                                          cache_token=True)

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
        self.response.status_code = http_client.INTERNAL_SERVER_ERROR
        self.requests = MagicMock(return_value=self.response)
        self.requests.get.side_effect = [self.response]

        with patch(self.session_get, self.requests):
            with self.assertRaises(ECSClientException):
                self.token_request.get_new_token()

    def test_get_new_token_should_throw_ecsclientexception_401(self):
        self.response.status_code = http_client.UNAUTHORIZED
        self.requests = MagicMock(return_value=self.response)
        self.requests.get.side_effect = [self.response]

        with patch(self.session_get, self.requests):
            with self.assertRaises(ECSClientException):
                self.token_request.get_new_token()
