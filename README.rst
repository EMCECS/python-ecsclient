ECS Minion
==========

ECS Minion is a Python library for interacting with the ECS 2.x Management API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://travis-ci.org/chadlung/ecsminion.svg?branch=master
    :target: https://travis-ci.org/chadlung/ecsminion

**Note:** `ECS <https://www.emc.com>`__ is an EMC product,
trademarked, copyrighted, etc.

This library follows the ECS API documentation `located here. <https://www.emc.com/techpubs/api/ecs/v2-0-0-0/index.htm>`__

Using this library is pretty straight forward. ECSMinion can be installed
from `PyPi <http://pypi.python.org/>`__:

::

    $ pip install ecsminion

Creating an instance of the ECSMinion class allows the following
arguments:

+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Name                  | Required   | Default Value     | Description                                                                                                                                   |
+=======================+============+===================+===============================================================================================================================================+
| ``username``          | No         | None              | The username used to fetch the ECS token                                                                                                      |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``password``          | No         | None              | The password used to fetch the ECS token                                                                                                      |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``token``             | No         | None              | Pass a token to ECSMinion (username/password are ignored then)                                                                                |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``ecs_endpoint``      | Yes        | None              | The ECS API endpoint, ex: ``https://192.168.0.149:4443``                                                                                      |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``token_endpoint``    | Yes        | None              | The ECS API endpoint, ex: ``https://192.168.0.149:4443/login``                                                                                |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``verify_ssl``        | No         | False             | Whether to check a host's SSL certificate                                                                                                     |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``token_filename``    | No         | ``ecstoken.tkn``  | The filename of the temporary token                                                                                                           |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``token_location``    | No         | ``/tmp``          | The location to store the temporary token file                                                                                                |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``request_timeout``   | No         | 15.0              | Stop waiting for a response after a given number of seconds, this is a decimal value. Ex: 10.0 is ten seconds                                 |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``cache_token``       | No         | True              | Whether to cache the token, by default this is true you should only switch this to false when you want to directly fetch a token for a user   |
+-----------------------+------------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+

Here is an example that goes through most of the API calls. Please note
that some calls take longer to complete than others. Sometimes you may
need to set your ``request_timeout`` to ``60.0``.

::

    from ecsminion import ECSMinion, ECSMinionException

    try:
        client = ECSMinion(username='ecsadmin@internal',
                           password='PASSWORD',
                           token_endpoint='https://192.168.0.149:4443/login',
                           ecs_endpoint='https://192.168.0.149:4443',
                           request_timeout=15.0)

        print(client.user_info.whoami())

        # Configuration
        print(client.certificate.get_certificate_chain())
        print(client.configuration_properties.get_properties(category='ALL'))
        print(client.configuration_properties.get_properties_metadata())
        print(client.licensing.add_license(license=data_dict))
        print(client.licensing.get_license())

        # User Management
        print(client.secret_key.create_new_secret_key('user1'))
        print(client.secret_key.get_user_secret_keys(uid='user1'))
        print(client.secret_key.get_user_secret_keys(
            uid='user1', namespace='namespace1'))
        print(client.user_object.get_object_users('namespace1'))
        print(client.user_object.get_object_user_info('user1'))
        print(client.user_object.get_object_user_info('user1', 'namespace1'))
        print(client.user_object.add_object_user(
            uid='user2', namespace='namespace1', tags=['mytag1', 'mytag1']))
        print(client.user_object.deactivate_object_user(
            uid='user2', namespace='namespace1'))
        print(client.user_object.get_object_user_info('user1'))
        print(client.user_object.lock_object_user('user1', True, 'namespace1'))
        print(client.user_object.get_object_user_lock('user1', 'namespace1'))
        print(client.user_object.lock_object_user('user1', False, 'namespace1'))
        print(client.user_object.get_object_user_lock('user1', 'namespace1'))
        print(client.authentication_provider.get_authentication_providers())
        print(client.authentication_provider.get_authentication_provider(
            'urn:AuthProvider:317843ad-71eb-4a86-b1bd-806f4275008a'))

        # Support
        print(client.call_home.get_connectemc_config())

        # Multi-tenancy
        print(client.namespace.get_namespaces())
        print(client.namespace.get_namespaces('namespace1'))
        print(client.namespace.get_retention_classes('namespace1'))
        print(client.namespace.create_retention_class('the-name', 2, 'namespace2'))
        print(client.namespace.update_retention_class('the-name', 199, 'namespace2'))
        print(client.namespace.get_namespace_quota('namespace1'))
        print(client.namespace.update_namespace_quota(2, 2, 'namespace1'))

        # Monitoring
        print(client.capacity.get_cluster_capacity())
        print(client.events.get_audit_events(
            '2015-06-08T01:00', '2015-06-09T00:00', 'namespace1'))
        # With a marker and a limit param (marker has been shortened)
        print(client.events.get_audit_events(
            '2015-06-08T01:00', '2015-06-09T00:00', 'namespace1', limit=3,
            marker='CIbS7YbdKRI4dXJuOnN0bTRkYzYtOWUxNy03MGFkYzAzMWUxNDQ='))
        # Only a few of the dashboard APIs are shown, there are more
        print(client.dashboard.get_local_zone())
        print(client.dashboard.get_local_zone_replication_groups())
        print(client.dashboard.get_local_zone_rglinks_failed())
        print(client.dashboard.get_local_zone_storage_pools())
        print(client.dashboard.get_local_zone_nodes())
        print(client.dashboard.get_node_processes('172.29.3.148'))
        print(client.dashboard.get_local_zone_replication_group_bootstrap_links())

        # Provisioning
        print(client.node.get_nodes())
        print(client.bucket.create_bucket(bucket_name='bucket-test1', namespace='namespace1'))
        print(client.bucket.deactivate_bucket(bucket_name='bucket-test1', namespace='namespace1'))
        print(client.bucket.get_buckets(namespace='namespace1'))
        print(client.bucket.set_bucket_retention(bucket_name='bucket-test1', namespace='namespace1'))
        print(client.bucket.get_bucket_retention(bucket_name='bucket-test1', namespace='namespace1'))
        print(client.bucket.get_bucket_info(bucket_name='bucket-test1', namespace='namespace1'))
        print(client.bucket.update_bucket_owner(bucket_name='bucket-test1', new_owner='user2', namespace='namespace1'))
        print(client.bucket.update_bucket_is_stale_allowed(bucket_name='bucket-test1', is_stale_allowed=False, namespace='namespace1'))
        print(client.bucket.get_bucket_lock(bucket_name='bucket-test1', namespace='namespace1'))
        # For the following is_locked must be passed as 'true' or 'false', not True/False
        print(client.bucket.set_lock_bucket(bucket_name='bucket-test1', is_locked='false', namespace='namespace1'))
        print(client.bucket.update_bucket_quota(bucket_name='bucket-test1', block_size=1, notification_size=2, namespace='namespace1'))
        print(client.bucket.get_bucket_quota(bucket_name='bucket-test1', namespace='namespace1'))
        print(client.bucket.delete_bucket_quota(bucket_name='bucket-test1', namespace='namespace1'))
        print(client.bucket.get_bucket_acl(bucket_name='bucket-test1', namespace='namespace1'))
        print(client.bucket.get_acl_permissions())
        print(client.bucket.get_acl_groups())
        print(client.base_url.get_all_configured_base_urls())
        print(client.base_url.get_base_url('urn:ObjectBaseUrl:6c74e6fb-a2a1-4386-bc25-b4399a6e74ce'))
        print(client.base_url.create_base_url('TestBaseURL', 'test.com', False))
        print(client.base_url.modify_base_url('urn:ObjectBaseUrl:19c391eb-37f4-4c65-a7a9-474668f71607',
                                              'SomeBaseURL', 'test.org', False))
        print(client.base_url.delete_base_url('urn:ObjectBaseUrl:19c391eb-37f4-4c65-a7a9-474668f71607'))
        print(client.data_store.get_data_store_list())
        print(client.data_store.get_commodity_data_store_associated_wth_storage_pool('192.29.3.51'))
        print(client.data_store.get_commodity_data_store_associated_wth_varray('urn:storageos:VirtualArray:3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37'))
        print(client.storage_pool.get_virtual_arrays()  # Local VDC
        print(client.storage_pool.get_virtual_arrays(vdc_id='urn:storageos:VirtualDataCenterData:a9faea85-d377-4a42-b5f1-fa15829f0c33'))
        print(client.storage_pool.get_virtual_array('urn:storageos:VirtualArray:3c4e8cca-2e3d-4f8d-b183-1c69ce2d5b37'))
        print(client.storage_pool.add_virtual_array(name='Varray1', description='Test storage pool 1'))
        print(client.virtual_data_center.get_all_vdcs())
        print(client.virtual_data_center.get_vdc_by_id('urn:storageos:VirtualDataCenterData:a9faea85-d377-4a42-b5f1-fa15829f0c33'))
        print(client.virtual_data_center.get_local_vdc())
        print(client.virtual_data_center.get_local_vdc_secret_key())
        print(client.virtual_data_center.get_vdc_by_name('tiva01'))
        print(client.virtual_data_center.insert_vdc_attributes('vdc1', '10.247.179.200', '1234secret'))
        print(client.virtual_data_center.deactivate_vdc('urn:storageos:VirtualDataCenterData:a9faea85-d377-4a42-b5f1-fa15829f0c33'))
        print(client.management_object.create_local_user_info('newadminuser', 'password', True, True))
        print(client.management_object.modify_local_user_info('newadminuser', 'password2', False, True))
        print(client.management_object.delete_local_user_info('newadminuser'))
        print(client.management_object.get_local_management_users())
        print(client.management_object.get_local_user_info('admin'))

        # Geo Replication
        print(client.replication_group.get_replication_groups())
        print(client.replication_group.get_replication_group(
            'urn:storageos:ReplicationGroupInfo:c2b0d3c4-c778-4a24-8da5-6a89784c4eeb:global'))
        print(client.replication_group.update_replication_group(
            'urn:storageos:ReplicationGroupInfo:c2b0d3c4-c778-4a24-8da5-6a89784c4eeb:global',
            'a-name' 'the-description', True)
        print(client.temp_failed_zone.get_all_temp_failed_zones())
        print(client.temp_failed_zone.get_temp_failed_zone(
            'urn:storageos:ReplicationGroupInfo:c2b0d3c4-c778-4a24-8da5-6a89784c4eeb:global'))

        # Metering/Billing
        print(client.billing.get_bucket_billing_info('bucket-test', 'namespace1'))
        print(client.billing.get_namespace_billing_info('namespace1', include_bucket_detail=True))
        print(client.billing.get_namespace_billing_sample(
            'namespace1', start_time='2015-06-15T00:00',
            end_time='2015-06-15T1:00', include_bucket_detail=True))
        print(client.billing.get_bucket_billing_sample(
            'bucket-test', 'namespace1',
            start_time='2015-06-15T00:00', end_time='2015-06-15T1:00'))

    except ECSMinionException as ecsminion_ex:
        print('Message: {0}'.format(ecsminion_ex.message))
        print('Status Code Returned: {0}\n'.format(ecsminion_ex.http_status_code))
        print('ECS API Message: {0}'.format(ecsminion_ex.ecs_message))
    except Exception as ex:
        print(ex.message)

Example: Uploading an ECS license
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

According to ECS API documentation, a call to ``POST /license`` should contain
a payload like the following:

::

    {
        "license_feature": [
            {
                "serial": "",
                "version": "",
                "issued_date": "",
                "expiration_date": "",
                "model": "",
                "product": "",
                "site_id": "",
                "issuer": "",
                "notice": "",
                "licensed_ind": "",
                "expired_ind": "",
                "license_id_indicator": "",
                "error_message": "",
                "storage_capacity_unit": "",
                "storage_capacity": "",
                "trial_license_ind": ""
            }
        ],
        "license_text": ""
    }

Thus, if you consume a JSON file with such license data, you may upload it
using the ``licensing.add_license()`` method:

::

    import json
    import pprint

    pp = pprint.PrettyPrinter()

    try:
        with open("ECS2.1_License.json") as data:
            license = json.load(data)

        pp.pprint(client.licensing.add_license(license))

    except ValueError as val_ex:  # includes simplejson.decoder.JSONDecodeError
        print("Couldn't parse JSON data: {0}".format(val_ex.message))
    except ECSMinionException as ecsminion_ex:
        print('Message: {0}'.format(ecsminion_ex.message))
        print('Status Code Returned: {0}\n'.format(ecsminion_ex.http_status_code))
        print('ECS API Message: {0}'.format(ecsminion_ex.ecs_message))
    except Exception as ex:
        print(ex.message)

Example: Enable logging output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ECSMinion leverages the Python ``logging`` module. Enable it from your
application like so:

::

    import logging

    # Default to INFO level logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

Now ECSMinion will tell you about what it's doing (and so will the
``requests`` library).  If you'd like even more information about the
HTTP requests and headers, use the following:

::

    import logging
    import httplib

    # Default to DEBUG level logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    # Show HTTP headers and payloads
    httplib.HTTPConnection.debuglevel = 1

If you don't want to see *any* ``requests`` logging, either filter it with
a ``logging`` filter or change the logging level for just that library:

::

    import logging

    # Default to INFO level logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Only show errors from requests lib
    logging.getLogger('requests.packages.urllib3').setLevel(logging.ERROR)


Example: Use a valid token instead of supplying a username and password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You pass an authentication token directly to ECSMinion which means you
don't need to supply a username/password. Here is an example (the token
has been shortened):

::

    client = ECSMinion(token='ALAcbGZtbjh6eVB3eUF1TzFEZWNmc0M2VVl2QjBVPQM',
                       token_endpoint='https://192.168.1.146:4443/login',
                       ecs_endpoint='https://192.168.1.146:4443',
                       request_timeout=15.0)

Example: Fetching tokens
^^^^^^^^^^^^^^^^^^^^^^^^

Fetching a token for a user can be done as follows by setting the
``cache_token`` parameter to false and then calling ``get_token``:

::

    from ecsminion import ECSMinion, ECSMinionException


    if __name__ == "__main__":
        try:
            client = ECSMinion(username='someone',
                               password='password',
                               token=None,
                               token_endpoint='https://192.168.1.146:4443/login',
                               ecs_endpoint='https://192.168.1.146:4443',
                               request_timeout=15.0,
                               cache_token=False)

            print(client.get_token())

        except ECSMinionException as ecsminion_ex:
            print('Message: {0}'.format(ecsminion_ex.message))
            print('Status Code Returned: {0}\n'.format(ecsminion_ex.http_status_code))
            print('ECS API Message: {0}'.format(ecsminion_ex.ecs_message))
        except Exception as ex:
            print(ex.message)

Example: Removing a cached token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    from ecsminion import ECSMinion, ECSMinionException


    if __name__ == "__main__":
        try:
            client = ECSMinion(username='someone',
                               password='password',
                               token=None,
                               token_endpoint='https://192.168.1.146:4443/login',
                               ecs_endpoint='https://192.168.1.146:4443',
                               request_timeout=15.0,
                               cache_token=False)

            print(client.remove_cached_token())

        except ECSMinionException as ecsminion_ex:
            print('Message: {0}'.format(ecsminion_ex.message))
            print('Status Code Returned: {0}\n'.format(ecsminion_ex.http_status_code))
            print('ECS API Message: {0}'.format(ecsminion_ex.ecs_message))
        except Exception as ex:
            print(ex.message)

License
^^^^^^^

This software library is released to you under the Apache License 2.0. See
`LICENSE <https://github.com/chadlung/ecsminion/blob/master/LICENSE>`__
for more information.
