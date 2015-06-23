
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
        params = {
            'force': force
        }

        if force:
            logout_resp = self.conn.get('logout', params=params)
        else:
            logout_resp = self.conn.get('logout')

        # Remove cached authorization token from disk, as the session is
        # now terminated.
        self.conn.remove_cached_token()

        return logout_resp
