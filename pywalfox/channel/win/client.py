import logging
from ..connector import Connector


class Client(Connector):
    """UDP-socket client used to communicate with the daemon."""
    def __init__(self):
        Connector.__init__(self, 'win32', False)

    def connect(self, host):
        """
        Connects to the UDP socket.

        :return: if the connection to the socket was successfull
        :rType: bool
        """
        try:
            self.socket.connect(host)
            logging.debug('Successfully connected to UDP socket at: %s:%s' % (host[0], host[1]))
            return True
        except Exception as e:
            logging.debug('Failed to connect to socket: %s' % str(e))

        return False
