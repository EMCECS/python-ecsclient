# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class AuthenticationProvider(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_authentication_providers(self):
        """
        Lists the configured authentication providers.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'authnprovider': [
                {
                    u'id': u'urn: AuthProvider:
                            fe4843f3-71eb-4a86-b1bd-806f4275998b',
                    u'name': u'internal'
                }
            ]
        }
        """
        log.info('Getting all authentication providers')
        return self.conn.get(url='vdc/admin/authnproviders')

    def get_authentication_provider(self, auth_provider_id):
        """
        Lists the configured authentication providers.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'search_scope': u'ONELEVEL',
            u'group_whitelist_values': [

            ],
            u'remote': None,
            u'name': u'internal',
            u'tags': [

            ],
            u'manager_dn': u'uid=admin,
            cn=users,
            cn=accounts,
            dc=osaas-lab,
            dc=rcsops,
            dc=com',
            u'max_page_size': 0,
            u'search_base': u'cn=users,
            cn=accounts,
            dc=osaas-lab,
            dc=rcsops,
            dc=com',
            u'global': None,
            u'group_attribute': u'CN',
            u'server_urls': [
                u'ldaps: //192.29.62.18: 636/',
                u'ldaps: //192.29.62.83: 636/',
                u'ldaps: //192.29.62.84: 636/',
                u'ldaps: //192.29.62.19: 636/'
            ],
            u'vdc': None,
            u'disable': False,
            u'mode': u'ldap',
            u'domains': [
                u'tenantadmins',
                u'internal'
            ],
            u'search_filter': u'uid=%U',
            u'id': u'urn: AuthProvider: 317843ad-71eb-4a86-b1bd-806f4275008a',
            u'description': u'internal'
        }

        param: auth_provider_id: Authentication provider identifier URN
        """
        log.info("Getting auth provider '{0}'".format(auth_provider_id))

        return self.conn.get(
            url='vdc/admin/authnproviders/{0}'.format(auth_provider_id))
