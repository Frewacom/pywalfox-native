import os
import socket

from pywalfox.config import SOCKET_PATH

class Connector:
    """Base class for UNIX-socket client and server."""
    def __init__(self):
        self.path = SOCKET_PATH
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

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
        encoded_message = self.encoded_message(message)
        self.socket.send(encoded_message)



