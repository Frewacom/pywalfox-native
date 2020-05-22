import sys
import json
import struct
import logging

from .config import DAEMON_VERSION, ACTIONS

class Messenger:
    """
    Handles the sending and receiving of messages to and from the extension using stdio.

    :param version str: the current major python version
    """
    def __init__(self, version):
        self.stdout, self.stdin = self.get_stdio_handle(version)

    def get_stdio_handle(self, python_version):
        """
        Gets the stdin and stdout handles depending on the current python version.
        Python 2.x uses 'sys.stdout.xxx', whereas python 3.x uses 'sys.stdout.buffer.xxx'.

        :return: (stdout handle, stdin handle) based on the current python version
        :rType: tuple
        """
        if python_version == 2:
            return (sys.stdout, sys.stdin)
        else:
            return (sys.stdout.buffer, sys.stdin.buffer)

    def decode_message(self, encoded_length):
        """
        Decodes a message received from stdin.

        :param encoded_length buffer: the buffer containing the data length
        :return: the decoded message
        :rType: object
        """
        data_length = struct.unpack('@I', encoded_length)[0]
        message = self.stdin.read(data_length).decode('utf-8')
        return json.loads(message)

    def encode_message(self, message):
        """
        Encodes a message to be sent to stdout.

        :param message object: the message to encode
        :return: (length of encoded message, encoded message)
        :rType: tuple
        """
        json_string = json.dumps(message).encode('utf-8')
        buffer_length = struct.pack('@I', len(json_string))
        return (buffer_length, json_string)

    def get_message(self):
        """
        Reads message from extension in stdin.

        :return: the decoded message
        :rType: str
        """
        encoded_length = self.stdin.read(4)
        if not encoded_length:
            sys.exit(0)

        return self.decode_message(encoded_length)

    def send_message(self, message_object):
        """
        Sends a message to stdout.

        :param message [Message|ErrorMessage]: the message to encode and send
        """
        length, encoded_message = self.encode_message(message_object.getMessage())
        self.stdout.write(length)
        self.stdout.write(encoded_message)
        self.stdout.flush()










