import testtools
from requests_mock.contrib import fixture
from mock import MagicMock
from mock import mock
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

    @mock.patch('ecsclient.common.token_request.TokenRequest.get_token')
    def test_list_nodes_throw_exception(self, mock_get_token):
        self.requests_mock.register_uri('GET', 'https://127.0.0.1:4443/vdc/nodes',
                                        status_code=http_client.INTERNAL_SERVER_ERROR,
                                        text='Server Error')
        mock_get_token.return_value = 'FAKE-TOKEN-123'

        with super(testtools.TestCase, self).assertRaises(ECSClientException) as error:
            self.client.node.list()

        exception = error.exception
        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, 'https://127.0.0.1:4443/vdc/nodes')
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'FAKE-TOKEN-123')
        self.assertEqual(exception.http_response_content, 'Server Error')
        self.assertEqual(exception.http_status, http_client.INTERNAL_SERVER_ERROR)

    @mock.patch('ecsclient.common.token_request.TokenRequest.get_token')
    def test_list_nodes(self, mock_get_token):
        mock_get_token.return_value = 'FAKE-TOKEN-123'
        self.requests_mock.register_uri('GET', 'https://127.0.0.1:4443/vdc/nodes',
                                        status_code=http_client.OK,
                                        json=self.returned_json)

        response = self.client.node.list()

        self.assertEqual(self.requests_mock.last_request.method, 'GET')
        self.assertEqual(self.requests_mock.last_request.url, 'https://127.0.0.1:4443/vdc/nodes')
        self.assertEqual(self.requests_mock.last_request.headers['x-sds-auth-token'], 'FAKE-TOKEN-123')
        self.assertEqual(response, self.returned_json)
