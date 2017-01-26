# Standard lib imports
import unittest

# Third party imports
from mock import MagicMock
from mock import patch
from six.moves import http_client

# Project level imports
from ecsclient.client import Client
from ecsclient.common.exceptions import ECSClientException


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(WhenTestingNode())
    return test_suite


class WhenTestingNode(unittest.TestCase):

    def setUp(self):
        self.ecs_endpoint = 'https://127.0.0.1:4443'
        self.token_endpoint = 'https://127.0.0.1:4443/login'

        self.client = Client(
            '2',
            ecs_endpoint=self.ecs_endpoint,
            token_endpoint=self.token_endpoint
        )

        self.returned_json = {
            "node": [
                {
                    "ip": "172.29.3.148",
                    "version": "1.2.0.0.60071.ffbe16c",
                    "rackId": "gray",
                    "nodename": "supr01-r01-01.lax01s1.rspaas-lab.ops.com",
                    "nodeid": "171.29.3.140"
                },
                {
                    "ip": "172.29.3.149",
                    "version": "1.2.0.0.60071.ffbe16c",
                    "rackId": "gray",
                    "nodename": "supr01-r01-02.lax01s1.rspaas-lab.ops.com",
                    "nodeid": "171.29.3.141"
                }
            ]
        }

        self.response = MagicMock()

    def test_get_nodes_should_throw_ecsclientexception(self):
        self.response.status_code = http_client.INTERNAL_SERVER_ERROR
        self.requests = MagicMock(return_value=self.response)
        self.requests.get.side_effect = [self.response]

        with patch('ecsclient.common.token_request.TokenRequest.get_new_token',
                   return_value='FAKE-TOKEN-123'):
            with patch('ecsclient.common.token_request.requests.Session.get'):
                with self.assertRaises(ECSClientException):
                    self.client.node.get_nodes()

    def test_get_nodes(self):
        self.response.status_code = http_client.OK
        self.response.body = self.returned_json
        self.response.json = MagicMock(return_value=self.returned_json)
        self.requests = MagicMock(return_value=self.response)
        self.requests.get.side_effect = [self.response]

        with patch('ecsclient.common.token_request.TokenRequest.'
                   '_get_existing_token', return_value='FAKE-TOKEN-123'):
            with patch('ecsclient.baseclient.requests.Session.get', self.requests):
                returned_json = self.client.node.get_nodes()
                self.assertEqual(returned_json, self.returned_json)

if __name__ == '__main__':
    unittest.main()
