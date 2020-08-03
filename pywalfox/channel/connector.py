import os
import socket
import logging
from ..config import UNIX_SOCKET_PATH, WIN_SOCKET_HOST, UNIX_SOCKET_PATH_ALT, WIN_SOCKET_HOST_ALT

class Connector:
    """
    Base class for the socket server and client.
    Depending on the current OS, a different socket type will be used,
    since UNIX-sockets are not properly supported on Windows.

    :param platform_id str: the current platform identifier, e.g. win32
    """
    def __init__(self, platform_id):
        if platform_id == 'win32':
            self.host = self.get_win_socket_host()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            logging.debug('Setup socket server using AF_INET (win32)')
        else:
            self.host = self.get_unix_socket_path()
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            logging.debug('Setup socket server using AF_UNIX (linux/darwin)')

    def get_unix_socket_path(self):
        """
        Get an available path to bind the UNIX-socket to.

        :return: the path to be used when binding the UNIX-socket
        :rType: str
        """
        if os.path.exists(UNIX_SOCKET_PATH):
            logging.debug('Default UNIX-socket is already in use')
            return UNIX_SOCKET_PATH_ALT

        return UNIX_SOCKET_PATH

    def get_win_socket_host(self):
        """
        Get an available host and port to bind the UDP-socket to.

        :return: the host and port to be used when binding the UDP-socket
        :rType: (host, port)
        """
        is_valid = True
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            test_socket.bind(WIN_SOCKET_HOST)
            test_socket.close()
        except OSError as e:
            is_valid = False
            if e.errno == 98: # errno 98 means that address is already bound
                logging.debug('Default UDP-socket host is already in use')
            else:
                logging.error('Failed to test UDP-socket host availability: %s' % str(e))

        if is_valid is True:
            return WIN_SOCKET_HOST

        return WIN_SOCKET_HOST_ALT

    def encode_message(self, message):
        """
        Encodes a message to be sent using the socket.

        :param message str: the message to encode into a bytestring
        :return: the encoded message
        :rType: bytestring
        """
        return message.encode('utf-8')

    def decode_message(self, raw):
        """
        Decodes a message received from the socket.

        :param raw bytestring: the raw message of bytes to decode
        :return: the decoded message
        :rType: str
        """
        return raw.decode('utf-8')

    def get_message(self):
        """
        Reads and decodes an incoming message.

        :return: the decoded data
        :rType: str
        """
        data = self.socket.recv(1024)
        if not data:
            logging.error('Failed to read data from socket')
            return

        return self.decode_message(data)

    def send_message(self, message):
        """
        Encodes and sends a message using the socket

        :param data str: the string to send
        """
        encoded_message = self.encode_message(message)
        self.socket.send(encoded_message)

    def close(self):
        """Closes the socket connection."""
        self.socket.close()
