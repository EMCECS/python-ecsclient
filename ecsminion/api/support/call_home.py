# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class CallHome(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_connectemc_config(self):
        """
        Gets ConnectEMC configuration details.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            "port": "25",
            "password": "",
            "transpport": "SMTP",
            "bsafe_encryption_ind": "no",
            "email_server": "mailhub.lss.emc.com",
            "email_sender": "someone@email.com",
            "notify_email_address": "johndoe@nowhere.com",
            "smtp_auth_type": "",
            "username": "",
            "start_tls_ind": "no",
            "enable_tls_cert": "no"
        }
        """

        return self.conn.get(url='vdc/callhome/connectemc/config')
