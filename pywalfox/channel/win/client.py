import logging
from ..connector import Connector


class Client(Connector):
    """UDP-socket client used to communicate with the daemon."""
    def __init__(self):
        Connector.__init__(self, 'win32')

    def start(self):
        """
        Connects to the UDP socket.

        :return: if the connection to the socket was successfull
        :rType: bool
        """
        try:
            self.socket.connect(self.host)
            logging.debug('Successfully connected to UDP socket at: %s:%s' % (self.host[0], self.host[1]))
            return True
        except Exception as e:
            logging.error('Failed to connect to socket: %s' % str(e))

        return False
