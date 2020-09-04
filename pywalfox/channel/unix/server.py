import os
import logging
from ..connector import Connector


class Server(Connector):
    """UNIX-socket server used to communicate with clients."""
    def __init__(self):
        Connector.__init__(self, 'unix')

    def delete_existing_socket(self):
        """Deletes the existing UNIX-socket if it exists."""
        if os.path.exists(self.host):
            os.remove(self.host)

    def start(self):
        """
        Binds the socket to file.

        :return: if the socket could be bound to the file
        :rType: bool
        """
        self.delete_existing_socket()
        try:
            self.socket.bind(self.host)
            logging.debug('Successfully bound socket to: %s' % self.host)
            return True
        except OSError as e:
            logging.error('Failed to create UNIX socket: %s' % e.strerror)

        return False

    def close(self):
        """Unbinds the socket and deletes the file."""
        self.socket.close()

        try:
            """
            UNIX-sockets can be overwritten by other processes even if another process
            is already using it. This may lead to the file not existing and will
            cause a crash if not handled properly.
            """
            os.remove(self.host)
            logging.debug('UNIX-socket deleted')
        except OSError as e:
            logging.debug('UNIX-socket has already been deleted, skipping')
