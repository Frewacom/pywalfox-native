import os
import socket
import logging

from connector import Connector

class Server(Connector):
    """UNIX-socket server used to communicate with clients."""
    def delete_existing_socket(self):
        """Deletes the existing UNIX-socket if it exists."""
        if os.path.exists(self.path):
            os.remove(self.path)

    def start(self):
        """
        Binds the socket to file.

        :return: if the socket could be bound to the file
        :rType: bool
        """
        self.delete_existing_socket()
        try:
            self.socket.bind(self.path)
            logging.debug('Successfully bound socket to %s' % self.path)
            return True
        except OSError as e:
            logging.error('Failed to create UNIX socket %s' % e.strerror)
            return False

    def close(self):
        """Unbinds the socket and deletes the file."""
        self.socket.close()
        os.remove(self.path)

