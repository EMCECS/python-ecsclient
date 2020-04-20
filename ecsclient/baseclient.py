import json
import logging
import os

import requests

from ecsclient.authentication import Authentication
from ecsclient.common.exceptions import ECSClientException
from ecsclient.common.token_request import TokenRequest

# Suppress the insecure request warning
# https://urllib3.readthedocs.org/en/
# latest/security.html#insecurerequestwarning
requests.packages.urllib3.disable_warnings()

# Initialize logger
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Client(object):

    def __init__(self, username=None, password=None, token=None,
                 ecs_endpoint=None, token_endpoint=None, verify_ssl=False,
                 token_path='/tmp/ecsclient.tkn',
                 request_timeout=15.0, cache_token=True, override_header=None):
        """
        Creates the ECSClient class that the client will directly work with

        :param username:
        The username to fetch a token
        :param password: The password to fetch a token
        :param token: Supply a valid token to use instead of username/password
        :param ecs_endpoint: The URL where ECS is located
        :param token_endpoint: The URL where the ECS login is located
        :param verify_ssl: Verify SSL certificates
        :param token_path: Path to the cached token file
        :param request_timeout: How long to wait for ECS to respond
        :param cache_token: Whether to cache the token, by default this is true
        you should only switch this to false when you want to directly fetch
        a token for a user
        :param override_header: X-EMC-Override header value into API calls
        """
        if not ecs_endpoint:
            raise ECSClientException("Missing 'ecs_endpoint'")

        self.token_endpoint = token_endpoint

        if token_endpoint:
            if not (username and password):
                raise ECSClientException("'token_endpoint' provided but missing ('username','password')")
            self.token_endpoint = self.token_endpoint.rstrip('/')
        else:
            if not (token or os.path.isfile(token_path)):
                raise ECSClientException("'token_endpoint' not provided and missing 'token'|'token_path'")

        self.override_header = override_header
        self.username = username
        self.password = password
        self.token = token
        self.ecs_endpoint = ecs_endpoint.rstrip('/')
        self.verify_ssl = verify_ssl
        self.token_path = token_path
        self.request_timeout = request_timeout
        self.cache_token = cache_token
        self._session = requests.Session()
        self._token_request = TokenRequest(
            username=self.username,
            password=self.password,
            ecs_endpoint=self.ecs_endpoint,
            token_endpoint=self.token_endpoint,
            verify_ssl=self.verify_ssl,
            token_path=self.token_path,
            request_timeout=self.request_timeout,
            cache_token=self.cache_token)

        # Authentication
        self.authentication = Authentication(self)

    def get_token(self):
        """
        Get a token directly back, typically you want to set the cache_token
        param for ecsclient to false for this call.

        :return: A valid token or an ecsclient exception
        """
        return self._token_request.get_new_token()

    def get_current_token(self):
        """
        Get the current token in use. None if the client is logged out or not yet logged in
        """
        return self._token_request.token

    def remove_cached_token(self):
        """
        Remove the cached token file, this is useful if you switch users
        and want to use a different token
        """
        self.token = None
        self._token_request.token = None

        if os.path.isfile(self.token_path):
            log.debug("Removing cached token '{0}'".format(self.token_path))
            os.remove(self.token_path)

    def _fetch_headers(self):
        token = self.token if self.token else self._token_request.get_token()
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'x-sds-auth-token': token}
        if self.override_header is not None:
            headers['X-EMC-Override'] = self.override_header
        return headers

    def _construct_url(self, path):
        url = '{0}/{1}'.format(self.ecs_endpoint, path)
        log.debug('Constructed URL as: {0}'.format(url))
        return url

    def get(self, url, params=None):
        return self._request(url, params=params)

    def post(self, url, json_payload='{}'):
        return self._request(url, json_payload, http_verb='POST')

    def put(self, url, json_payload='{}'):
        return self._request(url, json_payload, http_verb='PUT')

    def delete(self, url, params=None):
        return self._request(url, params=params, http_verb='DELETE')

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
            elif http_verb == 'DELETE':
                # Need to follow up - if 'accept' is in the headers
                # delete calls are not working because ECS 2.0 is returning
                # XML even if JSON is specified
                headers = self._fetch_headers()
                del headers['Accept']

                req = self._session.delete(
                    self._construct_url(url),
                    verify=self.verify_ssl,
                    headers=headers,
                    timeout=self.request_timeout,
                    params=params)
            else:  # Default to GET
                req = self._session.get(
                    self._construct_url(url),
                    verify=self.verify_ssl,
                    headers=self._fetch_headers(),
                    timeout=self.request_timeout,
                    params=params)

            # Because some delete actions in the API return HTTP/1.1 204 No Content
            if not (200 <= req.status_code < 300):
                log.error("Status code NOT OK")
                raise ECSClientException.from_response(req)
            try:
                return req.json()
            except ValueError:
                return req.text

        except requests.ConnectionError as conn_err:
            msg = 'Connection error: {0}'.format(conn_err.args)
            log.error(msg)
            raise ECSClientException(message=msg)
        except requests.HTTPError as http_err:
            msg = 'HTTP error: {0}'.format(http_err.args)
            log.error(msg)
            raise ECSClientException(message=msg)
        except requests.RequestException as req_err:
            msg = 'Request error: {0}'.format(req_err.args)
            log.error(msg)
            raise ECSClientException(message=msg)
