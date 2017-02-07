import logging

log = logging.getLogger(__name__)


class Cas(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_cas_secret(self, uid, namespace=None):
        """
        Gets CAS secret for the specified user and, optionally, a namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
          "user_cas_secret": { "cas_secret": "secret" }
        }

        :param uid: Valid user identifier to get the key from
        :param namespace: Namespace for which to get CAS secret
        """
        log.info("Fetching CAS secret for user ID '{uid}' (namespace '{namespace}')").format(
            uid=uid,
            namespace=namespace
        )
        if namespace:
            url = 'object/user-cas/secret/{namespace}/{uid}'.format(
                uid=uid,
                namespace=namespace
            )
        else:
            url = 'object/user-cas/secret/{uid}'.format(uid=uid)
        return self.conn.get(url)

    def set_cas_secret(self, uid, namespace, secret):
        """
        Creates or updates CAS secret for a specified user.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param uid: Valid user identifier to update a secret for
        :param namespace: Namespace identifier to associate with the CAS secret
        :param secret: Secret for the user
        """
        payload = {
          "user_cas_secret_param": {
            "namespace": namespace,
            "secret": secret
          }
        }

        log.info("Updating CAS secret for user ID '{}'".format(uid))
        return self.conn.post('object/user-cas/secret/{}'.format(uid), json_payload=payload)

    def delete_cas_secret(self, uid, namespace, secret):
        """
        Deletes CAS secret for a specified user identifier.

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        There is no response body for this call

        Expect: HTTP/1.1 200 OK

        :param uid: Valid user identifier to update a secret for
        :param namespace: Namespace identifier to associate with the CAS secret
        :param secret: CAS Secret for the user
        """
        payload = {
          "namespace": namespace,
          "secret": secret
        }

        log.info("Deleting CAS secret for user ID '{}'".format(uid))
        return self.conn.post('object/user-cas/secret/{}/deactivate'.format(uid), json_payload=payload)

    def generate_pea(self, uid, namespace):
        """
        Generates Pool Entry Authorization (PEA) file for specified user

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
          "pea": {
            "-version": "1.0.0",
            "defaultkey": {
              "-name": "wuser1@sanity.local",
              "credential": {
                "-id": "csp1.secret",
                "-enc": "base64",
                "#text": "c2VjcmV0"
              }
            },
            "key": {
              "-type": "cluster",
              "-id": "19999d80-37b2-3111-9c5d-7c053bc73f1a",
              "-name": "wuser1@sanity.local",
              "credential": {
                "-id": "csp1.secret",
                "-enc": "base64",
                "#text": "c2VjcmV0"
              }
            }
          }
        }

        :param uid: Valid user identifier to create PEA file
        :param namespace: Namespace id with CAS cluster
        """
        log.info("Generating Pool Entry Authorization (PEA) file for user ID '{uid}' (namespace '{namespace}')").format(
            uid=uid,
            namespace=namespace
        )
        return self.conn.get('object/user-cas/secret/{}/{}/pea'.format(uid, namespace))

    def get_default_bucket(self, uid, namespace=None):
        """
        Gets default bucket for the specified user identifier and, optionally, the namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
            "name": "standalone-bucket"
        }

        :param uid: Valid user identifier from which to get bucket
        :param namespace: Namespace from which to get bucket
        """
        log.info("Getting default bucket for user ID '{uid}' (namespace '{namespace}')").format(
            uid=uid,
            namespace=namespace
        )
        if namespace:
            url = '/object/user-cas/bucket/{namespace}/{uid}'.format(
                uid=uid,
                namespace=namespace
            )
        else:
            url = '/object/user-cas/bucket/{uid}'.format(uid=uid)
        return self.conn.get(url)

    def set_default_bucket(self, uid, namespace, bucket_name):
        """
        Updates default bucket the specified namespace and user identifier

        Required role(s):

        SYSTEM_ADMIN
        NAMESPACE_ADMIN

        Example JSON result from the API:

        {
          "user_cas_bucket": { "name": "standalone-bucket" }
        }

        :param uid: Valid user identifier to update default bucket
        :param namespace: Namespace required to update default bucket
        :param bucket_name: Name of the default bucket to be set
        """
        log.info("Setting default bucket to '{bucket_name}' for user ID '{uid}' (namespace '{namespace}')").format(
            uid=uid,
            namespace=namespace,
            bucket_name=bucket_name
        )
        payload = {
          "name": bucket_name
        }
        return self.conn.post('object/user-cas/bucket/{namespace}/{uid}'.format(
            uid=uid,
            namespace=namespace),
            json_payload=payload)

    def get_registered_applications(self, namespace):
        """
        Gets the CAS registered applications for a specified namespace.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:
        {}

        :param namespace: Namespace required to get CAS registered applications
        """
        # TODO: Add example JSON response

        log.info("Getting registered CAS applications on namespace '{namespace}'").format(
            namespace=namespace
        )
        return self.conn.get('object/user-cas/applications/{namespace}'.format(namespace=namespace))

    def get_user_metadata(self, uid, namespace):
        """
        Gets the CAS user metadata for the specified namespace and user identifier.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR
        NAMESPACE_ADMIN

        Example JSON result from the API:
        {
            "metadata": {},
            "user_name": "testlogin"
        }

        :param uid: User identifier for which to get metadata
        :param namespace: Namespace required to get metadata
        """

        log.info("Getting CAS user metadata for user ID '{uid}' (namespace '{namespace}')").format(
            uid=uid,
            namespace=namespace
        )
        return self.conn.get('object/user-cas/metadata/{namespace}/{uid}'.format(
            uid=uid,
            namespace=namespace))
