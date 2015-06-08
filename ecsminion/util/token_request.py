# Standard lib imports
import os

# Third party imports
import requests

# Project level imports
from ecsminion.util.exceptions import ECSMinionException


class TokenRequest(object):
    """
    This is a helper class to fetch a new token from the ECS controller
    and return the token as well as store it locally. Prior to fetching a new
    token we check if we have a local token and if so, whether or not it is
    still valid
    """

    def __init__(self, username, password, ecs_endpoint, token_endpoint,
                 verify_ssl, token_filename, token_location, request_timeout,
                 cache_token):
        """
        Create a new TokenRequest instance

        :param username: The username to fetch a token
        :param password: The password to fetch a token
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
        self.ecs_endpoint = ecs_endpoint
        self.token_endpoint = token_endpoint
        self.verify_ssl = verify_ssl
        self.token_verification_endpoint = ecs_endpoint + '/user/whoami'
        self.token_filename = token_filename
        self.token_location = token_location
        self.request_timeout = request_timeout
        self.cache_token = cache_token
        self.token_file = os.path.join(
            self.token_location, self.token_filename)
        self.session = requests.Session()

    def get_new_token(self):
        """
        Request a new authentication token from ECS and persist it
        to a file for future usage if cache_token is true

        :return: Returns a valid token, or None if failed
        """
        self.session.auth = (self.username, self.password)

        req = self.session.get(self.token_endpoint,
                               verify=self.verify_ssl,
                               headers={'Accept': 'application/json'},
                               timeout=self.request_timeout)

        if req.status_code == 401:
            raise ECSMinionException(
                http_status_code=req.status_code,
                message='Invalid username or password used')
        if req.status_code != 200:
            raise ECSMinionException(
                http_status_code=req.status_code)

        token = req.headers['x-sds-auth-token']

        if self.cache_token:
            with open(self.token_file, 'w') as token_file:
                token_file.write(token)

        return token

    def get_token(self):
        """
        Attempt to get an existing token, if successful then ensure it
        hasn't expired yet. If its expired, fetch a new token

        :return: A token
        """
        token = self._get_existing_token()

        if token:
            req = self._request(token, self.token_verification_endpoint)

            if req.status_code == requests.codes.ok:
                return token

        return self.get_new_token()

    def _get_existing_token(self):
        """
        Attempt to open and read the token file if it exists

        :return: If available return the token, if not return None
        """
        if os.path.isfile(self.token_file):
            with open(self.token_file, 'r') as token_file:
                return token_file.read()
        return None

    def _request(self, token, url):
        """
        Perform a request and place the token header inside the request header

        :param token: A valid token
        :param url:  The URL to perform a request
        :return: Request Object
        """
        headers = {'Accept': 'application/json',
                   'X-SDS-AUTH-TOKEN': token}
        try:
            return self.session.get(url, verify=self.verify_ssl,
                                    headers=headers,
                                    timeout=self.request_timeout)
        except requests.ConnectionError as conn_err:
            raise ECSMinionException(message=conn_err.message)
        except requests.HTTPError as http_err:
            raise ECSMinionException(message=http_err.message)
        except requests.RequestException as req_err:
            raise ECSMinionException(message=req_err.message)
