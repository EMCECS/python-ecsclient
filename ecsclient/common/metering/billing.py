import logging

log = logging.getLogger(__name__)


class Billing(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_bucket_billing_info(self, bucket_name, namespace, sizeunit='GB'):
        """
        Gets billing details for the specified namespace and bucket name.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'total_objects': 0,
            u'total_size_in_gb': 0.0,
            u'name': u'bucket-test',
            u'sample_time': u'2015-06-18T22: 20: 01Z',
            u'namespace': u'namespace1',
            u'vpool_id': u'urn: storageos: ReplicationGroupInfo:
                            4ea1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global',
            u'total_size_unit': u'GB'
        }

        :param bucket_name: Bucket name for which billing information needs
        to be retrieved
        :param namespace: Namespace containing the bucket
        :param sizeunit: Unit to be used for calculating the size on disk (KB,MB and GB. GB is default value)
        """
        log.info("Getting billing info for bucket '{0}'".format(bucket_name))

        params = {
            "sizeunit": sizeunit
        }

        return self.conn.get(
            url='object/billing/buckets/{0}/{1}/info'.format(
                namespace, bucket_name), params=params)

    def get_namespace_billing_info(self, namespace, sizeunit='GB',
                                   include_bucket_detail=False, marker=None):
        """
        Gets billing details for the specified namespace and bucket details.
        Note: Due to the fact that sampling a namespace's buckets takes some
        time it's possible that the values for the buckets will not sum to
        equal the namespace's values.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {{
            u'total_objects': 90,
            u'total_size_in_gb': 10.0,
            u'sample_time': u'2015-06-18T22: 28: 59Z',
            u'namespace': u'namespace1',
            u'bucket_billing_info': [
                {
                    u'vpool_id': u'urn: storageos: ReplicationGroupInfo:
                                4ea1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global',
                    u'total_size_unit': u'GB',
                    u'total_objects': 0,
                    u'total_size_in_gb': 0.0,
                    u'name': u'bucket-test1'
                },
                {
                    u'vpool_id': u'urn: storageos: ReplicationGroupInfo:
                                4ea1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global',
                    u'total_size_unit': u'GB',
                    u'total_objects': 90,
                    u'total_size_in_gb': 2.0,
                    u'name': u'large-uploads'
                }
            ],
            u'total_size_unit': u'GB',
            u'next_marker': u'test-302599c4-5ewd-44f3-b0dc-716ae3782dbd'
        }

        :param namespace: Namespace to get information about
        :param include_bucket_detail: Optional. (default=False). If True,
        include information about all the buckets owned by this namespace.
        :param marker: Optional. Used to continue a truncated response. Omit
        this parameter on the first request.
        :param sizeunit: Unit to be used for calculating the size on disk (KB,MB and GB. GB is default value)
        """
        log.info("Getting billing info for namespace '{0}'".format(namespace))

        params = {
            "include_bucket_detail": include_bucket_detail,
            "sizeunit": sizeunit
        }

        if marker:
            params['marker'] = marker

        return self.conn.get(
            url='object/billing/namespace/{0}/info'.format(
                namespace), params=params)

    def get_namespace_billing_sample(self, namespace, start_time, end_time, sizeunit='GB',
                                     include_bucket_detail=False, marker=None):
        """
        Gets billing details for the specified namespace, interval and bucket
        details. This method will return one and only one time sample. If the
        start_time and end_time do not align with a sampled time period, the
        matching samples will be aggregated.

        Check the response for the actual time period sampled. Due to the fact
        that sampling a namespace's buckets takes some time it is possible
        that the values for the buckets will not sum to equal the
        namespace's values.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'total_objects': 4707,
            u'total_size_in_gb': 10.0,
            u'bytes_delta': 0,
            u'bucket_billing_sample': [
                {
                    u'total_objects': 0,
                    u'total_size_in_gb': 0.0,
                    u'name': u'bucket-test1',
                    u'namespace': u'namespace1',
                    u'ingress': 0,
                    u'vpool_id': u'urn: storageos: ReplicationGroupInfo:
                                4ea1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global',
                    u'objects_created': 0,
                    u'egress': 0,
                    u'sample_start_time': u'2015-06-15T00: 00: 00Z',
                    u'objects_deleted': 0,
                    u'sample_end_time': u'2015-06-15T01: 00: 00Z',
                    u'total_size_unit': u'GB',
                    u'bytes_delta': 0
                },
                {
                    u'total_objects': 0,
                    u'total_size_in_gb': 0.0,
                    u'name': u'large-uploads',
                    u'namespace': u'namespace1',
                    u'ingress': 0,
                    u'vpool_id': u'urn: storageos: ReplicationGroupInfo:
                                4ea1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global',
                    u'objects_created': 0,
                    u'egress': 0,
                    u'sample_start_time': u'2015-06-15T00: 00: 00Z',
                    u'objects_deleted': 0,
                    u'sample_end_time': u'2015-06-15T01: 00: 00Z',
                    u'total_size_unit': u'GB',
                    u'bytes_delta': 0
                }
            ],
            u'namespace': u'namespace1',
            u'ingress': 0,
            u'objects_created': 0,
            u'egress': 0,
            u'sample_start_time': u'2015-06-15T00: 00: 00Z',
            u'objects_deleted': 0,
            u'sample_end_time': u'2015-06-15T01: 00: 00Z',
            u'total_size_unit': u'GB',
            u'next_marker': u'test-302599c4-5ewd-44f3-b0dc-716ae3782dbd'
        }

        :param namespace: Namespace to get information about
        :param include_bucket_detail: Optional. (default=False). If True,
        include information about all the buckets owned by this namespace.
        :param marker: Optional. Used to continue a truncated response. Omit
        this parameter on the first request.
        :param start_time: Starting time in ISO-8601 minute format
        :param end_time: Ending time in ISO-8601 minute format
        :param sizeunit: Unit to be used for calculating the size on disk (KB,MB and GB. GB is default value)
        """
        log.info("Sampling billing info for namespace '{0}'".format(namespace))

        params = {
            "include_bucket_detail": include_bucket_detail,
            "start_time": start_time,
            "end_time": end_time,
            "sizeunit": sizeunit
        }

        if marker:
            params['marker'] = marker

        return self.conn.get(
            url='object/billing/namespace/{0}/sample'.format(
                namespace), params=params)

    def get_bucket_billing_sample(self, bucket_name, namespace,
                                  start_time, end_time, sizeunit='GB'):
        """
        Gets billing details for the specified namespace, interval and bucket
        details. By default, buckets are sampled every 5 minutes. If the
        requested time range includes multiple samples, the data will be
        aggregated.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            u'total_objects': 0,
            u'total_size_in_gb': 0.0,
            u'name': u'bucket-test',
            u'namespace': u'namespace1',
            u'ingress': 0,
            u'vpool_id': u'urn: storageos: ReplicationGroupInfo:
                            4ea1fa1e-a7d1-4a8e-b8cc-e5a2c27f308d: global',
            u'objects_created': 0,
            u'egress': 0,
            u'sample_start_time': u'2015-06-15T00: 00: 00Z',
            u'objects_deleted': 0,
            u'sample_end_time': u'2015-06-15T01: 00: 00Z',
            u'total_size_unit': u'GB',
            u'bytes_delta': 0
        }

        :param namespace: Namespace containing the bucket
        :param bucket_name: Bucket name
        :param start_time: Starting time in ISO-8601 minute format
        :param end_time: Ending time in ISO-8601 minute format
        :param sizeunit: Unit to be used for calculating the size on disk (KB,MB and GB. GB is default value)s
        """
        log.info("Sampling billing info for bucket '{0}' in namespace "
                 "'{1}'".format(bucket_name, namespace))

        params = {
            "start_time": start_time,
            "end_time": end_time,
            "sizeunit": sizeunit
        }

        return self.conn.get(
            url='object/billing/buckets/{0}/{1}/sample'.format(
                namespace, bucket_name), params=params)
