# Standard lib imports
import json
import os

# Third party imports
import requests

# Project level imports
from ecsminion.api.authentication import Authentication

from ecsminion.api.configuration.certificate import Certificate
from ecsminion.api.configuration.configuration_properties \
    import ConfigurationProperties
from ecsminion.api.configuration.licensing import Licensing

from ecsminion.api.monitoring.capacity import Capacity
from ecsminion.api.monitoring.events import Events

from ecsminion.api.user_management.secret_key import SecretKey
from ecsminion.api.user_management.user_object import ObjectUser

from ecsminion.api.undocumented.user_info import UserInfo

from ecsminion.util.exceptions import ECSMinionException
from ecsminion.util.token_request import TokenRequest


# Suppress the insecure request warning
# https://urllib3.readthedocs.org/en/
# latest/security.html#insecurerequestwarning
requests.packages.urllib3.disable_warnings()


class ECSMinion(object):

    def __init__(self, username=None, password=None, token=None,
                 ecs_endpoint=None, token_endpoint=None, verify_ssl=False,
                 token_filename='ecsminion.tkn', token_location='/tmp',
                 request_timeout=15.0, cache_token=True):
        """
        Creates the ECSMinion class that the client will directly work with

        :param username: The username to fetch a token
        :param password: The password to fetch a token
        :param token: Supply a valid token to use instead of username/password
        :param ecs_endpoint: The URL where ECS is located
        :param token_endpoint: The URL where the ECS login is located
        :param verify_ssl: Verify SSL certificates
        :param token_filename: The name of the cached token filename
        :param token_location: By default this is stored in /tmp
        :param request_timeout: How long to wait for ECS to respond
        :param cache_token: Whether to cache the token, by default this is true
        you should only switch this to false when you want to directly fetch
        a token for a user
        """

        self.username = username
        self.password = password
        self.token = token
        self.ecs_endpoint = ecs_endpoint.rstrip('/')
        self.token_endpoint = token_endpoint.rstrip('/')
        self.verify_ssl = verify_ssl
        self.token_filename = token_filename
        self.token_location = token_location
        self.request_timeout = request_timeout
        self.cache_token = cache_token
        self._session = requests.Session()
        self._token_request = TokenRequest(
            username=self.username,
            password=self.password,
            ecs_endpoint=self.ecs_endpoint,
            token_endpoint=self.token_endpoint,
            verify_ssl=self.verify_ssl,
            token_filename=self.token_filename,
            token_location=self.token_location,
            request_timeout=self.request_timeout,
            cache_token=self.cache_token)
        self.token_file = os.path.join(
            self.token_location, self.token_filename)

        # API -> Authentication
        self.authentication = Authentication(self)

        # API -> Configuration
        self.certificate = Certificate(self)
        self.configuration_properties = ConfigurationProperties(self)
        self.licensing = Licensing(self)

        # Monitoring
        self.capacity = Capacity(self)
        self.events = Events(self)

        # API -> User Management
        self.secret_key = SecretKey(self)
        self.user_object = ObjectUser(self)

        # API -> Undocumented
        self.user_info = UserInfo(self)

    def get_token(self):
        """
        Get a token directly back, typically you want to set the cache_token
        param for ecsminion to false for this call.

        :return: A valid token or an ecsminion exception
        """
        return self._token_request.get_new_token()

    def remove_cached_token(self):
        """
        Remove the cached token file, this is useful if you switch users
        and want to use a different token
        """
        if os.path.isfile(self.token_file):
            os.remove(self.token_file)

    def _fetch_headers(self):
        if self.token:
            return {'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'x-sds-auth-token': self.token}
        else:
            return {'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'x-sds-auth-token': self._token_request.get_token()}

    def _construct_url(self, url):
        return '{0}/{1}'.format(self.ecs_endpoint, url)

    def get(self, url, params=None):
        return self._request(url, params=params)

    def post(self, url, json_payload='{}'):
        return self._request(url, json_payload, http_verb='POST')

    def put(self, url, json_payload='{}'):
        return self._request(url, json_payload, http_verb='PUT')

    def _request(self, url, json_payload='{}', http_verb='GET', params=None):
        json_payload = json.dumps(json_payload)

        try:
            if http_verb == "PUT":
                req = self._session.put(
                    self._construct_url(url),
                    verify=self.verify_ssl,
                    headers=self._fetch_headers(),
                    timeout=self.request_timeout,
                    data=json_payload)
            elif http_verb == 'POST':
                req = self._session.post(
                    self._construct_url(url),
                    verify=self.verify_ssl,
                    headers=self._fetch_headers(),
                    timeout=self.request_timeout,
                    data=json_payload)
            else:  # Default to GET
                req = self._session.get(
                    self._construct_url(url),
                    verify=self.verify_ssl,
                    headers=self._fetch_headers(),
                    timeout=self.request_timeout,
                    params=params)

            if req.status_code != 200:
                raise ECSMinionException(
                    http_status_code=req.status_code,
                    ecs_message=req.text)
            return req.json()

        except requests.ConnectionError as conn_err:
            raise ECSMinionException(message=conn_err.message)
        except requests.HTTPError as http_err:
            raise ECSMinionException(message=http_err.message)
        except requests.RequestException as req_err:
            raise ECSMinionException(message=req_err.message)
        except ValueError:
            return
