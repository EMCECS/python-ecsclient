ECS Minion
==========

ECS Minion is a library for interacting with the ECS 2.x Management API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://travis-ci.org/chadlung/ecsminion.svg?branch=master
    :target: https://travis-ci.org/chadlung/ecsminion

**Note:** `ECS <https://www.emc.com>`__ is an EMC product,
trademarked, copyrighted, etc.

This library follows the ECS API documentation `located here. <https://www.emc.com/techpubs/api/ecs/v2-0-0-0/index.htm>`__

Using this library is pretty straight forward. ECSMinion can be installed
from `PyPi <http://pypi.python.org/>`__:

::

    $ pip install ecsminion

Creating an instance of the ECSMinion class requires the following
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
        print(client.licensing.get_license())

        # User Management
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

        # Monitoring
        # print(client.capacity.get_cluster_capacity())
        print(client.events.get_audit_events(
            '2015-06-08T01:00', '2015-06-09T00:00', 'namespace1'))
        # With a marker and a limit param (marker has been shortened)
        print(client.events.get_audit_events(
            '2015-06-08T01:00', '2015-06-09T00:00', 'namespace1', limit=3,
            marker='CIbS7YbdKRI4dXJuOnN0bTRkYzYtOWUxNy03MGFkYzAzMWUxNDQ='))


    except ECSMinionException as ecsminion_ex:
        print('Message: {0}'.format(ecsminion_ex.message))
        print('Status Code Returned: {0}\n'.format(ecsminion_ex.http_status_code))
        print('ECS API Message: {0}'.format(ecsminion_ex.ecs_message))
    except Exception as ex:
        print(ex.message)

Running PEP8
------------

There are some example JSON comments in the source code that are over
the allowed PEP8 length. You can ignore those by running:

::

    $ pep8 --ignore=E501 .

License
-------

This software library is released to you under the Apache License 2.0. See
`LICENSE <https://github.com/chadlung/ecsminion/blob/master/LICENSE>`__
for more information.
