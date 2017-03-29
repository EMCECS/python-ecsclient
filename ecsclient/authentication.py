import logging

log = logging.getLogger(__name__)


class Authentication(object):
    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def logout(self, force=False):
        """
        Perform an HTTP GET against the ECS endpoint to
        log an authenticated user out, thereby invalidating their
        authentication token.

        Example JSON result from the API:

        {"user": "root"}

        :param force: If you have multiple sessions running simultaneously this
        forces the termination of all tokens to the current user
        """

        if not self.conn.get_current_token():
            log.warning('Not logging out since the client has no token set up')
            return

        params = {
            'force': force
        }

        log.info('Terminating session (signing out): {0}'.format(params))

        if force:
            logout_resp = self.conn.get('logout', params=params)
        else:
            logout_resp = self.conn.get('logout')

        # Remove cached authorization token from disk, as the session is
        # now terminated.
        self.conn.remove_cached_token()

        return logout_resp
