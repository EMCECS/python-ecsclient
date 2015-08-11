# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class BaseUrl(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_all_configured_base_urls(self):
        """
        Lists all configured Base URLs.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'base_url': [
                {
                    u'link': {
                        u'href': u'/object/baseurl/urn: ObjectBaseUrl:
                                    6c74e6fb-a2a1-4386-bc25-b4399a6e74ce',
                        u'rel': u'self'
                    },
                    u'name': u'US1',
                    u'id': u'urn: ObjectBaseUrl:
                                6c74e6fb-a2a1-4386-bc25-b4399a6e74ce'
                },
                {
                    u'link': {
                        u'href': u'/object/baseurl/urn: ObjectBaseUrl:
                                    70f63a6f-25be-432c-875f-61c4a3953c42',
                        u'rel': u'self'
                    },
                    u'name': u'DefaultBaseUrl',
                    u'id': u'urn: ObjectBaseUrl:
                                70f63a6f-25be-432c-875f-61c4a3953c42'
                },
                {
                    u'link': {
                        u'href': u'/object/baseurl/urn: ObjectBaseUrl:
                                    72863b71-27a8-4917-8df0-cc84d3bdfe98',
                        u'rel': u'self'
                    },
                    u'name': u'US2',
                    u'id': u'urn: ObjectBaseUrl:
                                72863b71-27a8-4917-8df0-cc84d3bdfe98'
                }
            ]
        }
        """
        log.info("Getting all Base URLs")
        return self.conn.get(url='object/baseurl')

    def get_base_url(self, base_url_id):
        """
        Gets details for the specified Base URL.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'remote': None,
            u'name': u'US1',
            u'tags': [

            ],
            u'global': None,
            u'baseUrlNamespaceInHostFlag': False,
            u'baseurl': u'os-us1.rraas-ops.com',
            u'vdc': None,
            u'link': {
                u'href': u'/object/baseurl/urn: ObjectBaseUrl:
                            6c74e6fb-a2a1-4386-bc25-b4399a6e74ce',
                u'rel': u'self'
            },
            u'id': u'urn: ObjectBaseUrl: 6c74e6fb-a2a1-4386-bc25-b4399a6e74ce'
        }

        :param base_url_id: Base URL identifier for the Base URL that needs to
        be retrieved
        """
        log.info("Getting Base URL '{0}'".format(base_url_id))
        return self.conn.get(url='object/baseurl/{0}'.format(base_url_id))

    def create_base_url(self, name, base_url, is_namespace_in_host=True):
        """
        Creates a Base URL with the given details.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        {
            u'remote': None,
            u'name': u'TestBaseURL',
            u'tags': [

            ],
            u'global': None,
            u'baseUrlNamespaceInHostFlag': False,
            u'baseurl': u'test.com',
            u'vdc': None,
            u'link': {
                u'href': u'/object/baseurl/urn: ObjectBaseUrl:
                            19c391eb-37f4-4c65-a7a9-474668f71607',
                u'rel': u'self'
            },
            u'id': u'urn: ObjectBaseUrl: 19c391eb-37f4-4c65-a7a9-474668f71607'
        }

        :param name: Name for this Base-URL
        :param base_url: Base URL to be used
        :param is_namespace_in_host: Set true if namespace is in host, false
        otherwise
        """
        payload = {
            "name": name,
            "base_url": base_url,
            "is_namespace_in_host": is_namespace_in_host
        }
        log.info("Creating Base URL '{0}': {1}".format(name, payload))
        return self.conn.post(url='object/baseurl', json_payload=payload)

    def delete_base_url(self, base_url_id):
        """
        Updates the owner for the specified bucket.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param base_url_id: Base URL identifier that needs to be deleted
        """
        log.info("Deleting Base URL '{0}'".format(base_url_id))

        return self.conn.post(
            url='object/baseurl/{0}/deactivate'.format(base_url_id))

    def modify_base_url(self, base_url_id, name, base_url,
                        is_namespace_in_host=True):
        """
        Updates the Base URL for the specified Base URL identifier.

        Required role(s):

        SYSTEM_ADMIN

        Example JSON result from the API:

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param base_url_id: Base URL identifier that needs to be updated
        :param name: Name for this Base-URL
        :param base_url: Base URL to be used
        :param is_namespace_in_host: Set true if namespace is in host, false
        otherwise
        """
        payload = {
            "name": name,
            "base_url": base_url,
            "is_namespace_in_host": is_namespace_in_host
        }

        log.info("Updating Base URL '{0}': {1}".format(base_url_id, payload))

        return self.conn.put(
            url='object/baseurl/{0}'.format(base_url_id), json_payload=payload)
