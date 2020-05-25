import os
import logging
from ..connector import Connector


class Client(Connector):
    """UNIX-socket client used to communicate with the daemon."""
    def __init__(self):
        Connector.__init__(self, 'unix')

    def start(self):
        """
        Connects to the UNIX-socket if it exists.

        :return: if the connection to the socket was successfull
        :rType: bool
        """
        if os.path.exists(self.host):
            try:
                self.socket.connect(self.host)
                logging.debug('Successfully connected to UNIX socket at: %s' % self.host)
                return True
            except OSError as e:
                logging.error('Failed to connect to socket: %s' % e.strerror)
        else:
            logging.error('Could not find socket: %s' % self.host)

        return False
