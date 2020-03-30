import os
import socket

class Connector:
    """
    Base class for UNIX-socket client and server.

    :param path str: file path to the UNIX-socket
    """
    def __init__(self, path):
        self.path = path
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
