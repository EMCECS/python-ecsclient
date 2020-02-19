# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class Dashboard(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_local_zone(self, *args, **kwargs):
        """
        Gets the local VDC details

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category', 'cfTimeFrame', 'cfTarget']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting local VDC info")
        return self.conn.get(url='dashboard/zones/localzone', params=param)

    def get_local_zone_replication_groups(self, *args, **kwargs):
        """
        Gets the local VDC replication groups details

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting vpools in local VDC")
        return self.conn.get(url='dashboard/zones/localzone/replicationgroups', params=param)

    def get_local_zone_rglinks_failed(self, *args, **kwargs):
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
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting failed links for vpools in local VDC")
        return self.conn.get(url='dashboard/zones/localzone/rglinksFailed')

    def get_local_zone_storage_pools(self, *args, **kwargs):
        """
        Gets the local VDC storage pool details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category', 'cfTimeFrame', 'cfTarget']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting varrays in local VDC")
        return self.conn.get(url='dashboard/zones/localzone/storagepools', params=param)

    def get_local_zone_nodes(self, *args, **kwargs):
        """
        Gets the local vdc node details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category', 'cfTimeFrame', 'cfTarget']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting nodes in local VDC")
        return self.conn.get(url='dashboard/zones/localzone/nodes', params=param)

    def get_storage_pool(self, storage_pool_id, *args, **kwargs):
        """
        Gets the storage pool details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param storage_pool_id: Storage pool identifier
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category', 'cfTimeFrame', 'cfTarget']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting info for varray '{0}'".format(storage_pool_id))

        return self.conn.get(
            url='dashboard/storagepools/{0}'.format(storage_pool_id), params=param)

    def get_node(self, node_id, *args, **kwargs):
        """
        Gets the node instance details

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param node_id: Node identifier
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category', 'cfTimeFrame', 'cfTarget']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting info for node '{0}'".format(node_id))

        return self.conn.get(
            url='dashboard/nodes/{0}'.format(node_id))

    def get_disk(self, disk_id, *args, **kwargs):
        """
        Gets the disk instance details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param disk_id: Storage pool identifier
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting info for disk '{0}'".format(disk_id))

        return self.conn.get(
            url='dashboard/disks/{0}'.format(disk_id), params=param)

    def get_process(self, process_id, *args, **kwargs):
        """
        Gets the process instance details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param process_id: Identity of the process
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting info for PID '{0}'".format(process_id))

        return self.conn.get(
            url='dashboard/processes/{0}'.format(process_id), params=param)

    def get_node_processes(self, node_id, *args, **kwargs):
        """
        Gets the node instance process details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param node_id: Identity of the process
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting processes for node '{0}'".format(node_id))

        return self.conn.get(
            url='dashboard/nodes/{0}/processes'.format(node_id), params=param)

    def get_node_disks(self, node_id, *args, **kwargs):
        """
        Gets the node instance disk details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param node_id: Identity of the node
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting disks for node '{0}'".format(node_id))

        return self.conn.get(
            url='dashboard/nodes/{0}/disks'.format(node_id), params=param)

    def get_storage_pool_nodes(self, storage_pool_id, *args, **kwargs):
        """
        Gets the storage pool node details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param storage_pool_id: Identity of the storage pool
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category', 'cfTimeFrame', 'cfTarget']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting nodes for varray '{0}'".format(storage_pool_id))

        return self.conn.get(
            url='dashboard/storagepools/{0}/nodes'.format(storage_pool_id), params=param)

    def get_local_zone_replication_group_bootstrap_links(self, *args, **kwargs):
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
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting vpool bootstrap links in local VDC")

        return self.conn.get(
            url='dashboard/zones/localzone/rglinksBootstrap', params=param)

    def get_replication_group(self, replication_group_id, *args, **kwargs):
        """
        Gets the replication group instance details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param replication_group_id: Replication group identifier
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting info for vpool '{0}'".format(replication_group_id))

        return self.conn.get(
            url='dashboard/replicationgroups/{0}'.format(replication_group_id), params=param)

    def get_replication_group_link(self, rglink_id, *args, **kwargs):
        """
        Gets the replication group link instance details

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param rglink_id: Replication group link identifier
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting info for vpool link '{0}'".format(rglink_id))
        return self.conn.get(url='dashboard/rglinks/{0}'.format(rglink_id), params=param)

    def get_replication_group_links(self, replication_group_id, *args, **kwargs):
        """
        Gets the replication group instance associated link details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        Too large to output here

        :param replication_group_id: Replication group identifier
        """
        keys = ['dataType', 'startTime', 'endTime', 'interval', 'category']

        param = {}
        for key in keys:
            value = kwargs.get(key)
            if value:
                param[key] = value
        log.info("Getting links for vpool '{0}'".format(replication_group_id))

        return self.conn.get(
            url='dashboard/replicationgroups/{0}/rglinks'.format(
                replication_group_id),
            params=param
        )
