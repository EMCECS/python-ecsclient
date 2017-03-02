import testtools
from requests_mock.contrib import fixture
from mock import MagicMock
from mock import mock
from mock import patch
from six.moves import http_client
from ecsclient.client import Client
from ecsclient.common.exceptions import ECSClientException


class TestNode(testtools.TestCase):

    def setUp(self):
        super(TestNode, self).setUp()
        self.ecs_endpoint = 'https://127.0.0.1:4443'
        self.token_endpoint = 'https://127.0.0.1:4443/login'

        self.client = Client(
            '2',
            ecs_endpoint=self.ecs_endpoint,
            token_endpoint=self.token_endpoint,
            username='user',
            password='password'
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
        self.requests_mock = self.useFixture(fixture.Fixture())

    @mock.patch('ecsclient.common.token_request.TokenRequest.get_new_token')
    def test_get_nodes_should_throw_ecsclientexception(self, mock_get_new_token):
        self.requests_mock.register_uri('GET', 'https://127.0.0.1:4443/vdc/nodes',
                                        status_code=http_client.INTERNAL_SERVER_ERROR,
                                        text='Server Error')
        mock_get_new_token.return_value = 'FAKE-TOKEN-123'

        with super(testtools.TestCase, self).assertRaises(ECSClientException) as error:
            self.client.node.get_nodes()

        exception = error.exception
        self.assertEqual(exception.http_response_content, 'Server Error')
        self.assertEqual(exception.http_status, http_client.INTERNAL_SERVER_ERROR)

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
