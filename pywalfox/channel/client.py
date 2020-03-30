import os
import socket
import logging

from pywalfox.channel.connector import Connector

class Client(Connector):
    """UNIX-socket client used to communicate with the daemon."""
    def __init__(self):
        Connector.__init__(self)

    def start(self):
        """
        Connects to the UNIX-socket if it exists.

        :return: if the connection to the socket was successfull
        :rType: bool
        """
        if os.path.exists(self.path):
            try:
                self.socket.connect(self.path)
                return True
            except OSError as e:
                logging.error('Failed to connect to socket: %s' % e.strerror)
        else:
            logging.error('Could not find socket: %s' % self.path)

        return False

    def send_message(self, message):
        """
        Sends a message via the socket.

        :param message str: the mesage to encode and send
        """
        raw_message = self.encode_message(message)
        self.socket.send(raw_message)

    def close(self):
         """Closes the socket connection."""
         self.socket.close()


