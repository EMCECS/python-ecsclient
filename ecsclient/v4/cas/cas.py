from ecsclient.common.cas import cas
import logging

log = logging.getLogger(__name__)


class Cas(cas.Cas):

    def update_cluster_id(self, cluster_id):
        """
        Updates the cluster ID

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param cluster_id: given cluster ID
        """
        log.info("Updating cluster ID '{}'".format(cluster_id))
        return self.conn.put('object/user-cas/cluster/{}'.format(cluster_id))
