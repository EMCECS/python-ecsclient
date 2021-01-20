import logging

log = logging.getLogger(__name__)

"""
Tenant APIs only supported in ECS Flex
"""


class Tenant(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def list(self):
        """
        Gets the identifiers for all configured tenants.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'tenant': [
                {
                    u'id': u'tenant1'
                }
            ]
        }
        """
        log.info("Getting all tenants")
        return self.conn.get(url='object/tenants')

    def get(self, tenant):
        """
        Gets the details for the given tenant.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        TENANT_ADMIN

        :param tenant: Tenant identifier for which details needs to
        be retrieved.
        """
        log.info("Getting info for tenant '{0}'".format(tenant))

        return self.conn.get(
            url='object/tenants/tenant/{0}'.format(tenant))

    def create(self, account, default_data_services_vpool=None,
               is_encryption_enabled=False, default_bucket_block_size=None):
        """
        Creates a namespace with the given details

       Required role(s):

       SYSTEM_ADMIN

       Example JSON result from the API:
       {
            'account_id':account_id,
            'default_data_services_vpool': default_data_services_vpool,
            'default_bucket_block_size': default_bucket_block_size
            'is_encryption_enabled': is_encryption_enabled
       }
       """
        payload = {
            'account_id': account,
            'default_bucket_block_size': default_bucket_block_size,
            'default_data_services_vpool': default_data_services_vpool,
            'is_encryption_enabled': is_encryption_enabled,
        }
        log.info("Creating tenant for account '{0}'".format(account))
        return self.conn.post('object/tenants/tenant', json_payload=payload)

    # def update(self, tenant_id, default_data_services_vpool=None, vpools_added_to_allowed_vpools_list=[],
    #            vpools_added_to_disallowed_vpools_list=[], vpools_removed_from_allowed_vpools_list=[],
    #            vpools_removed_from_disallowed_vpools_list=[], tenant_admins=None, user_mapping=None,
    #            default_bucket_block_size=None, external_group_admins=None, is_encryption_enabled=None,
    #            is_stale_allowed=None):
    #     """
    #     Updates tenant details like replication group list, tenant admins and user mappings.
    #     Replication group can be:
    #         - Added to allowed or disallowed replication group list
    #         - Removed from allowed or disallowed replication group list
    #
    #     Required role(s):
    #
    #     SYSTEM_ADMIN
    #     TENANT_ADMIN
    #
    #     There is no response body for this call
    #
    #     Expect: HTTP/1.1 200 OK
    #
    #     :param tenant_id: Tenant identifier whose details needs to be updated
    #     :param default_data_services_vpool: Default replication group identifier when creating buckets
    #     :param vpools_added_to_allowed_vpools_list: List of replication group identifier which will be added in the
    #     allowed List for allowing tenant access
    #     :param vpools_added_to_disallowed_vpools_list: List of replication group identifier which will be added in the
    #     disallowed list for prohibiting tenant access
    #     :param vpools_removed_from_allowed_vpools_list: List of replication group identifier which will be removed
    #     from allowed list
    #     :param vpools_removed_from_disallowed_vpools_list: List of replication group identifier which will be removed
    #     from disallowed list for removing their prohibition tenant access
    #     :param tenant_admins: Comma separated list of tenant admins
    #     :param user_mapping: List of user mapping objects
    #     :param default_bucket_block_size: Default bucket quota size
    #     :param external_group_admins: List of groups from AD Server
    #     :param is_encryption_enabled: Update encryption for the tenant. If null then encryption will not be updated.
    #     :param is_stale_allowed: Flag to allow stale data within the tenant. If null then stale allowance will not be
    #     updated
    #     """
    #     payload = {
    #         "default_data_services_vpool": default_data_services_vpool,
    #         "vpools_added_to_allowed_vpools_list": vpools_added_to_allowed_vpools_list,
    #         "vpools_added_to_disallowed_vpools_list": vpools_added_to_disallowed_vpools_list,
    #         "vpools_removed_from_allowed_vpools_list": vpools_removed_from_allowed_vpools_list,
    #         "vpools_removed_from_disallowed_vpools_list": vpools_removed_from_disallowed_vpools_list,
    #         "tenant_admins": tenant_admins,
    #         "user_mapping": user_mapping,
    #         "default_bucket_block_size": default_bucket_block_size,
    #         "external_group_admins": external_group_admins,
    #         "is_encryption_enabled": is_encryption_enabled,
    #         "is_stale_allowed": is_stale_allowed
    #     }
    #     # FIXME: According to the API, this call should return the updated object, but it does not
    #     log.info("Updating tenant ID '{}'".format(tenant_id))
    #     return self.conn.put('object/tenants/tenant/{}'.format(tenant_id), json_payload=payload)

    def delete(self, tenant_id):
        """
        Deactivates and deletes the given tenant.

        Required role(s):

        SYSTEM_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param tenant_id: An active tenant identifier which needs to be deleted
        """
        log.info("Deleting tenant ID '{}'".format(tenant_id))
        # FIXME: This should be a DELETE request
        return self.conn.post('object/tenants/tenant/{}/delete'.format(tenant_id))
