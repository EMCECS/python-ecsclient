import logging

from ecsclient.common.provisioning.node import Node

log = logging.getLogger(__name__)


class Node(Node):

    def get_vdc_lock_status(self):
        raise NotImplementedError()

    def set_vdc_lock_status(self):
        raise NotImplementedError()

    def get_node_lock_status(self):
        raise NotImplementedError()

    def set_node_lock_status(self):
        raise NotImplementedError()
