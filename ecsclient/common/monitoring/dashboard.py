import logging


log = logging.getLogger(__name__)


class Dashboard(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_local_zone(self):
        """
        Gets the local VDC details

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here
        """
        log.info("Getting local VDC info")
        return self.conn.get(url='dashboard/zones/localzone')

    def get_local_zone_replication_groups(self):
        """
        Gets the local VDC replication groups details

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here
        """
        log.info("Getting local VDC replication groups details")
        return self.conn.get(url='dashboard/zones/localzone/replicationgroups')

    def get_local_zone_rglinks_failed(self):
        """
        Gets the local VDC replication group failed links details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'_embedded': {
                u'_instances': [

                ]
            },
            u'_links': {
                u'self': {
                    u'href': u'/dashboard/zones/localzone/rglinksFailed'
                }
            },
            u'title': u'rglinksFailedList'
        }
        """
        log.info("Getting failed links for vpools in local VDC")
        return self.conn.get(url='dashboard/zones/localzone/rglinksFailed')

    def get_local_zone_storage_pools(self):
        """
        Gets the local VDC storage pool details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here
        """
        log.info("Getting varrays in local VDC")
        return self.conn.get(url='dashboard/zones/localzone/storagepools')

    def get_local_zone_nodes(self):
        """
        Gets the local vdc node details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here
        """
        log.info("Getting nodes in local VDC")
        return self.conn.get(url='dashboard/zones/localzone/nodes')

    def get_storage_pool(self, storage_pool_id):
        """
        Gets the storage pool details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param storage_pool_id: Storage pool identifier
        """
        log.info("Getting info for varray '{0}'".format(storage_pool_id))

        return self.conn.get(
            url='dashboard/storagepools/{0}'.format(storage_pool_id))

    def get_node(self, node_id):
        """
        Gets the node instance details

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param node_id: Node identifier
        """
        log.info("Getting info for node '{0}'".format(node_id))

        return self.conn.get(
            url='dashboard/nodes/{0}'.format(node_id))

    def get_disk(self, disk_id):
        """
        Gets the disk instance details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param disk_id: Storage pool identifier
        """
        log.info("Getting info for disk '{0}'".format(disk_id))

        return self.conn.get(
            url='dashboard/disks/{0}'.format(disk_id))

    def get_process(self, process_id):
        """
        Gets the process instance details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param process_id: Identity of the process
        """
        log.info("Getting info for PID '{0}'".format(process_id))

        return self.conn.get(
            url='dashboard/processes/{0}'.format(process_id))

    def get_node_processes(self, node_id):
        """
        Gets the node instance process details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param node_id: Identity of the process
        """
        log.info("Getting processes for node '{0}'".format(node_id))

        return self.conn.get(
            url='dashboard/nodes/{0}/processes'.format(node_id))

    def get_node_disks(self, node_id):
        """
        Gets the node instance disk details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param node_id: Identity of the node
        """
        log.info("Getting disks for node '{0}'".format(node_id))

        return self.conn.get(
            url='dashboard/nodes/{0}/disks'.format(node_id))

    def get_storage_pool_nodes(self, storage_pool_id):
        """
        Gets the storage pool node details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param storage_pool_id: Identity of the storage pool
        """
        log.info("Getting nodes for varray '{0}'".format(storage_pool_id))

        return self.conn.get(
            url='dashboard/storagepools/{0}/nodes'.format(storage_pool_id))

    def get_local_zone_replication_group_bootstrap_links(self):
        """
        Gets the local VDC replication group bootstrap links details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'_embedded': {
                u'_instances': [

                ]
            },
            u'_links': {
                u'self': {
                    u'href': u'/dashboard/zones/localzone/rglinksBootstrap'
                }
            },
            u'title': u'rglinksBootstrapList'
        }
        """
        log.info("Getting vpool bootstrap links in local VDC")

        return self.conn.get(
            url='dashboard/zones/localzone/rglinksBootstrap')

    def get_replication_group(self, replication_group_id):
        """
        Gets the replication group instance details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param replication_group_id: Replication group identifier
        """
        log.info("Getting info for vpool '{0}'".format(replication_group_id))

        return self.conn.get(
            url='dashboard/replicationgroups/{0}'.format(replication_group_id))

    def get_replication_group_link(self, rglink_id):
        """
        Gets the replication group link instance details

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param rglink_id: Replication group link identifier
        """
        log.info("Getting info for vpool link '{0}'".format(rglink_id))
        return self.conn.get(url='dashboard/rglinks/{0}'.format(rglink_id))

    def get_replication_group_links(self, replication_group_id):
        """
        Gets the replication group instance associated link details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param replication_group_id: Replication group identifier
        """
        log.info("Getting links for vpool '{0}'".format(replication_group_id))

        return self.conn.get(
            url='dashboard/replicationgroups/{0}/rglinks'.format(
                replication_group_id)
        )
