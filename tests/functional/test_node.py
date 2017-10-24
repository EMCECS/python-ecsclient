from ecsclient import schemas
from tests import functional


class TestNode(functional.BaseTestCase):

    def test_node_list(self):
        response = self.client.node.list()
        self.assertValidSchema(response, schemas.NODE_LIST)
