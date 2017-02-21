# Standard lib imports
import logging

# Third party imports
# None

# Project level imports
# None


log = logging.getLogger(__name__)


class ConfigurationProperties(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_properties(self, category='ALL'):
        """
        Gets the configuration properties for the specified category. If the
        category is not provided, then properties of all categories will
        be retrieved

        :param category:  The category for which to retrieve configuration
        properties. If this is not provided it defaults to "ALL"

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'allProperties': {
                u'user_scope': u'GLOBAL'
            },
            u'properties': {
                u'user_scope': u'GLOBAL'
            },
            u'empty': False
        }

        """
        log.info("Getting configurations in category '{0}'".format(category))
        return self.conn.get(
            'config/object/properties?category={0}'.format(category))

    def get_properties_metadata(self):
        """
        Gets the meta data for each of the configuration properties.
        Metadata includes the possible values for the property, a description
        of the property, whether a reboot is required when it is changed, etc.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'metadata': {
                u'user_scope': {
                    u'reconfigRequired': False,
                    u'description': u'Declaresthescopeforusernameuniqueness',
                    u'userMutable': False,
                    u'minLen': 0,
                    u'userConfigurable': False,
                    u'defaultValue': None,
                    u'controlNodeOnly': False,
                    u'value': u'GLOBAL',
                    u'allowedValues': [
                        u'NAMESPACE',
                        u'GLOBAL'
                    ],
                    u'maxLen': 65534,
                    u'defaultValueMetaData': u'GLOBAL',
                    u'hidden': False,
                    u'label': u'Userscope',
                    u'type': u'string',
                    u'rebootRequired': False,
                    u'advanced': False
                }
            }
        }

        """
        log.info("Getting metadata properties")
        return self.conn.get('config/object/properties/metadata')

    def set_properties(self):
        """
        Sets the configuration properties for the system.

        Properties are:
        user-scope: defines whether user accounts should be treated as GLOBAL
        or NAMESPACE.

        In GLOBAL scope, users are global and are can be shared across
        namespaces. In this case, the default namespace associated with a user
        determines the namespace for object operations and there is no need to
        supply a namespace for an operation.

        If the user scope is NAMESPACE, a user is associated with a namespace,
        so there might be more than user with the same name, each associated
        with a different namespace. In NAMESPACE mode a namespace must be
        provided for every operation. Must be set before the first user is
        created.

        The default setting is GLOBAL.
        """
        log.error("Configuration properties modification not supported")
        raise NotImplementedError
