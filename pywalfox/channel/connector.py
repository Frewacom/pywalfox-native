import socket
import logging
from ..config import UNIX_SOCKET_PATH, WIN_SOCKET_HOST


class Connector:
    """
    Base class for the socket server and client.
    Depending on the current OS, a different socket type will be used,
    since UNIX-sockets are not properly supported on Windows.

    :param platform_id str: the current platform identifier, e.g. win32
    """
    def __init__(self, platform_id):
        if platform_id == 'win32':
            self.host = WIN_SOCKET_HOST
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            logging.debug('Setup socket server using AF_INET (win32)')
        else:
            self.host = UNIX_SOCKET_PATH
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            logging.debug('Setup socket server using AF_UNIX (linux/darwin)')

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
