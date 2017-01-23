# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class ECSClientException(Exception):
    """
    This is a custom ECSClientException Exception class to better handle
    errors that ECSClientException can return in HTML format rather than JSON
    """

    def __init__(self, message=None, http_status_code=None, ecs_message=None):
        """
        This is a custom ECSClientException class to handle

        :param message: A custom
        :param http_status_code:
        :param ecs_message:
        :return:
        """
        if message is None:
            self.message = 'The ECSClientException endpoint has thrown ' \
                           'an error, check the http_status_code and ' \
                           'ecs_message attributes of this exception for ' \
                           'more details.'
        else:
            self.message = message

        self.http_status_code = http_status_code
        self.ecs_message = ecs_message

        super(ECSClientException, self).__init__(
            message, http_status_code, ecs_message)
