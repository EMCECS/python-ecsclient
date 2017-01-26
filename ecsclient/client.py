import logging

import ecsclient.v2.client as v2_client

_logger = logging.getLogger(__name__)

_CLIENT_VERSIONS = {'2': v2_client.Client}


def Client(version=None, *args, **kwargs):
    """Factory function to create a new ECS client.

    The returned client will be either a V3 or V2 client. Check the version
    using the :py:attr:`~ecsclient.v2.client.Client.version` property or
    the instance's class (with instanceof).

     :param string version: The required version of the ECS Management API.
    """

    if not version:
        msg = ("Please provide the API version. Options are: '2', '3'."
               "http://$HOST:$PORT/v$VERSION_NUMBER")
        raise RuntimeError(msg)

    try:
        client_class = _CLIENT_VERSIONS[version]
    except KeyError:
        msg = ('No client available for version: %s') % version
        raise RuntimeError(msg)

    return client_class(*args, **kwargs)
