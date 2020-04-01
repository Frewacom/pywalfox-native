import os
import socket
import logging

from ..connector import Connector

class Server(Connector):
    """UDP-socket server used to communicate with clients."""
    def __init__(self):
        Connector.__init__(self, 'win32')

    def start(self):
        """
        Binds the socket to localhost.

        :return: if the socket could be bound to the host
        :rType: bool
        """
        try:
            self.socket.bind(self.host)
            logging.debug('Successfully bound socket to: %s:%s' % (self.host[0], self.host[1]))
            return True
        except OSError as e:
            logging.error('Failed to setup UDP socket server: %s' % e.strerror)
        
        return False

