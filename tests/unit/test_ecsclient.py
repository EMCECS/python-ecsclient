import unittest

import mock

from ecsclient import v2, v3
from ecsclient.client import Client
from ecsclient.common.exceptions import ECSClientException


class TestEcsClient(unittest.TestCase):

    def test_client_without_version(self):
        with self.assertRaises(RuntimeError) as error:
            Client(username='user',
                   password='password',
                   ecs_endpoint='https://192.168.1.10',
                   token_endpoint='https://192.168.10/login')
        exception = error.exception
        self.assertIn('Please provide the API version', str(exception))

    def test_client_unsupported_version(self):
        with self.assertRaises(RuntimeError) as error:
            Client(version='10',
                   username='user',
                   password='password',
                   ecs_endpoint='https://192.168.1.10',
                   token_endpoint='https://192.168.10/login')
        exception = error.exception
        self.assertEqual("No client available for version '10'", str(exception))

    def test_client_without_ecs_endpoint(self):
        with self.assertRaises(ECSClientException) as error:
            Client(version='3',
                   username='user',
                   password='password',
                   token_endpoint='https://192.168.10/login')
        exception = error.exception.message
        self.assertEqual("Missing 'ecs_endpoint'", str(exception))

    def test_client_without_token_endpoint(self):
        with self.assertRaises(ECSClientException) as error:
            Client(version='3',
                   username='user',
                   password='password',
                   ecs_endpoint='https://192.168.1.10')
        exception = error.exception.message
        self.assertEqual("'token_endpoint' not provided and missing 'token'|'token_path'", str(exception))

    def test_client_without_credentials(self):
        with self.assertRaises(ECSClientException) as error:
            Client(version='3',
                   ecs_endpoint='https://192.168.1.10',
                   token_endpoint='https://192.168.10/login')
        exception = error.exception.message
        self.assertEqual("'token_endpoint' provided but missing ('username','password')", str(exception))

    def test_client_v3_class(self):
        c = Client(version='3',
                   username='user',
                   password='password',
                   ecs_endpoint='https://192.168.1.10',
                   token_endpoint='https://192.168.10/login')
        self.assertIsInstance(c, v3.client.Client, 'Instance is not a v3 client class')

    def test_client_v2_class(self):
        c = Client(version='2',
                   username='user',
                   password='password',
                   ecs_endpoint='https://192.168.1.10',
                   token_endpoint='https://192.168.10/login')
        self.assertIsInstance(c, v2.client.Client, 'Instance is not a v2 client class')

    def test_client_init_with_credentials(self):
        c = Client(version='3',
                   username='user',
                   password='password',
                   token_endpoint='https://192.168.10/login',
                   ecs_endpoint='https://192.168.1.10')
        self.assertTrue(hasattr(c, 'username'))
        self.assertTrue(hasattr(c, 'password'))
        self.assertTrue(hasattr(c, 'token_endpoint'))

    def test_client_init_with_token(self):
        c = Client(version='3',
                   token='1234567890',
                   ecs_endpoint='https://192.168.1.10')
        self.assertTrue(hasattr(c, 'token'))

    @mock.patch('ecsclient.baseclient.os.path.isfile')
    def test_client_init_with_token_path(self, mock_isfile):
        mock_isfile.return_value = True
        c = Client(version='3',
                   token_path='/tmp/token.tkn',
                   ecs_endpoint='https://192.168.1.10')
        self.assertTrue(hasattr(c, 'token_path'))
