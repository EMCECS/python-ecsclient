================
python-ecsclient
================

|Build_Status| |Docs| |Python| |Version| |Coverage|

This library is the Python Software Development Kit (SDK) for `Dell EMC ECS
<https://www.emc.com/en-us/storage/ecs/index.htm>`_.
It allows developers to interact with the ECS Management API. You can find
the ECS API specification `here <https://www.emc.com/techpubs/api/ecs/v3-0-0-0/index.htm>`_.

This library is the successor of `ECS Minion
<https://github.com/chadlung/ecsminion>`_.


.. |Build_Status| image:: https://travis-ci.org/EMCECS/python-ecsclient.svg?branch=master
    :target: https://travis-ci.org/EMCECS/python-ecsclient
    :alt: Build Status
.. |Docs| image:: https://readthedocs.org/projects/python-ecsclient/badge/?version=latest&style=flat
    :target: https://python-ecsclient.readthedocs.io/en/latest/
    :alt: Read the docs
.. |Version| image:: https://img.shields.io/pypi/v/python-ecsclient.svg
    :target: https://pypi.python.org/pypi/python-ecsclient/
    :alt: Version
.. |Python| image:: https://img.shields.io/pypi/pyversions/python-ecsclient.svg
    :target: https://pypi.python.org/pypi/python-ecsclient/
    :alt: Python Versions
.. |Coverage| image:: https://coveralls.io/repos/github/EMCECS/python-ecsclient/badge.svg?branch=master
    :target: https://coveralls.io/github/EMCECS/python-ecsclient?branch=master
    :alt: Coverage
.. |License| image:: http://img.shields.io/pypi/l/python-ecsclient.svg?style=flat
    :target: https://github.com/EMCECS/python-ecsclient/blob/master/LICENSE
    :alt: License
.. _`documentation`: https://python-ecsclient.readthedocs.io/en/latest/
.. _`v2`: https://www.emc.com/techpubs/api/ecs/v2-2-1-0/index.htm
.. _`v3`: https://www.emc.com/techpubs/api/ecs/v3-0-0-0/index.htm

Quick Start
-----------

You can install ``python-ecsclient`` using pip.

.. code-block:: sh

    $ pip install python-ecsclient

Creating an instance of the ECSClient class allows the following
arguments:

+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Name                  | Required   | Default Value          | Description                                                                                                                                   |
+=======================+============+========================+===============================================================================================================================================+
| ``version``           | Yes        | None                   | Version of the target ECS system. Options are ``2``, ``3`` and ``4``                                                                          |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``username``          | No         | None                   | The username used to fetch the ECS token                                                                                                      |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``password``          | No         | None                   | The password used to fetch the ECS token                                                                                                      |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``token``             | No         | None                   | Pass a token to ECSClient (username/password are ignored then)                                                                                |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``ecs_endpoint``      | Yes        | None                   | The ECS API endpoint, ex: ``https://192.168.0.149:4443``                                                                                      |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``token_endpoint``    | No         | None                   | The ECS API endpoint, ex: ``https://192.168.0.149:4443/login``                                                                                |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``verify_ssl``        | No         | False                  | Whether to check a host's SSL certificate                                                                                                     |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``token_path``        | No         | ``/tmp/ecsclient.tkn`` | The location to store the temporary token file                                                                                                |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``request_timeout``   | No         | 15.0                   | Stop waiting for a response after a given number of seconds, this is a decimal value. Ex: 10.0 is ten seconds                                 |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``cache_token``       | No         | True                   | Whether to cache the token, by default this is true you should only switch this to false when you want to directly fetch a token for a user   |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``override_header``   | No         | None                   | Add X-EMC-Override header with the header value in API request only if it is not None
  |
+-----------------------+------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
This is how you can instantiate the ``Client`` class and use the library.

.. code-block:: python

    from ecsclient.client import Client

    client = Client('3',
                    username='ecsadmin@internal',
                    password='PASSWORD',
                    token_endpoint='https://192.168.0.149:4443/login',
                    ecs_endpoint='https://192.168.0.149:4443')

    print(client.user_info.whoami())

Take a look at our `documentation`_ to find a list of all supported ECS endpoints and services.

Supply a token
~~~~~~~~~~~~~~
You can pass an authentication token directly to the client which means you
don't need to supply a username/password.

.. code-block:: python

    client = Client('3',
                    token='ALAcbGZtbjh6eVB3eUF1TzFEZWNmc0M2VVl2QjBVPQM',
                    ecs_endpoint='https://192.168.1.146:4443')


Token caching
~~~~~~~~~~~~~
By default, the client caches the auth token. But you can disable caching
by setting the ``cache_token`` parameter to false.

.. code-block:: python

    client = Client('3',
                    username='someone',
                    password='password',
                    token_endpoint='https://192.168.1.146:4443/login',
                    ecs_endpoint='https://192.168.1.146:4443',
                    cache_token=False)

Alternatively, when token caching is enabled, you may want to force the client
to obtain a new token on the next call. To do so, you can remove the cached token.

.. code-block:: python

    client.remove_cached_token()

Add X-EMC-Override: "true" header
~~~~~~~~~~~~~~
You can pass override_header to the client which means the user wants to add custom 
X-EMC-Override header into API request

.. code-block:: python

    client = Client('3',
                    username='someone',
                    password='password',
                    token_endpoint='https://192.168.1.146:4443/login',
                    ecs_endpoint='https://192.168.1.146:4443',
                    override_header='true')


Supported endpoints
-------------------

The following table shows the supported endpoints per API version.

+--------------------------+---------+---------+---------+
|                          |  `v2`_  |  `v3`_  |  `v4`_  |
+==========================+=========+=========+=========+
| **Configuration**                                      |
+--------------------------+---------+---------+---------+
| Certificate              |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Configuration Properties |    ✓*   |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| Licensing                |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Feature                  |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Syslog                   |         |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| Snmp                     |         |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| **CAS**                                                |
+--------------------------+---------+---------+---------+
| CAS User Profile         |    ✓*   |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| **File System Access**                                 |
+--------------------------+---------+---------+---------+
| NFS                      |    ✗    |    ✗    |    ✗    |
+--------------------------+---------+---------+---------+
| **Metering**                                           |
+--------------------------+---------+---------+---------+
| Billing                  |    ~    |    ~    |    ~    |
+--------------------------+---------+---------+---------+
| **Migration**                                          |
+--------------------------+---------+---------+---------+
| Transformation           |    ✗    |    ✗    |    ✗    |
+--------------------------+---------+---------+---------+
| **Monitoring**                                         |
+--------------------------+---------+---------+---------+
| Capacity                 |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Dashboard                |    ✓*   |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| Events                   |    ✓*   |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| Alerts                   |    ✓*   |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| **Multi-tenancy**                                      |
+--------------------------+---------+---------+---------+
| Namespace                |    ✓*   |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| Tenant(Flex)             |    ✗    |    ✗    |    ✓*   |
+--------------------------+---------+---------+---------+
| **Geo-Replication**                                    |
+--------------------------+---------+---------+---------+
| Replication Group        |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Temporary Failed Zone    |    ✓*   |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| **Provisioning**                                       |
+--------------------------+---------+---------+---------+
| Base URL                 |    ✓*   |    ✓*   |    ✓*   |
+--------------------------+---------+---------+---------+
| Bucket                   |    ✓*   |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Data Store               |    ✓*   |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Node                     |    ~    |    ~    |    ~    |
+--------------------------+---------+---------+---------+
| Storage Pool             |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Virtual Data Center      |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| VDC Keystore             |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| **Support**                                            |
+--------------------------+---------+---------+---------+
| Call Home                |    ✗    |    ✗    |    ✗    |
+--------------------------+---------+---------+---------+
| **User Management**                                    |
+--------------------------+---------+---------+---------+
| Authentication Provider  |    ~    |    ~    |    ~    |
+--------------------------+---------+---------+---------+
| Password Group (Swift)   |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Secret Key               |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| Secret Key Self-Service  |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| User (Object)            |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| User (Management)        |    ✓*   |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+
| **Other**                                              |
+--------------------------+---------+---------+---------+
| Who am I                 |    ✓    |    ✓    |    ✓    |
+--------------------------+---------+---------+---------+

**Legend:**

+-------+-------------------------------------+
|   ✓   | Supported and tested                |
+-------+-------------------------------------+
|   ✓*  | Supported but not tested yet        |
+-------+-------------------------------------+
|   ~   | Partially supported                 |
+-------+-------------------------------------+
|   ✗   | Not supported yet                   |
+-------+-------------------------------------+
|       | Not available in this API version   |
+-------+-------------------------------------+

Development
-----------

Getting Started
~~~~~~~~~~~~~~~
Assuming that you have Python and ``virtualenv`` installed, set up your
environment and install the required dependencies like this instead of
the ``pip install python-ecsclient`` defined above:

.. code-block:: sh

    $ git clone https://github.com/EMCECS/python-ecsclient.git
    $ cd python-ecsclient
    $ virtualenv venv
    ...
    $ . venv/bin/activate
    $ pip install -r requirements.txt

Running Tests
~~~~~~~~~~~~~
You can run tests in all supported Python versions using ``tox``. By default,
it will run all of the unit tests, but you can also specify your own
``nosetests`` options. Note that this requires that you have all supported
versions of Python installed, otherwise you must pass ``-e`` or run the
``nosetests`` command directly:

.. code-block:: sh

    $ tox
    $ tox -e py27,py35 tests/functional

You can also run individual tests with your default Python version:

.. code-block:: sh

    $ nosetests tests/unit

License
-------

This software library is released to you under the Apache License 2.0. See
`LICENSE <https://github.com/EMCECS/python-ecsclient/blob/master/LICENSE>`__
for more information.

----------

`ECS <https://www.emc.com>`__ is an Dell EMC product,
trademarked, copyrighted, etc.
