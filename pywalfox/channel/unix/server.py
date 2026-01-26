import os
import socket
import logging
from ..connector import Connector


class Server(Connector):
    """UNIX-socket server used to communicate with clients."""
    def __init__(self):
        Connector.__init__(self, 'unix')

    def is_socket_in_use(self):
        """Check if the socket is actively in use by another process."""
        if not os.path.exists(self.host):
            return False

        test_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        try:
            test_socket.connect(self.host)
            test_socket.close()
            return True
        except (socket.error, OSError):
            return False

    def delete_existing_socket(self):
        """Deletes the existing UNIX-socket if it exists and is stale."""
        if os.path.exists(self.host):
            if self.is_socket_in_use():
                logging.error('Another daemon is already running')
                return False
            os.remove(self.host)
        return True

    def start(self):
        """
        Binds the socket to file.

        :return: if the socket could be bound to the file
        :rType: bool
        """
        if not self.delete_existing_socket():
            return False
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
