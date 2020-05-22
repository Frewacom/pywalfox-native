import sys
import logging
from threading import Thread

from .fetcher import *
from .custom_css import *

from .config import *
from .response import Message
from .messenger import Messenger

if sys.platform.startswith('win32'):
    from .channel.win.server import Server
else:
    from .channel.unix.server import Server

class Daemon:
    """
    Implements the daemon functionality that communicates with the extension.

    :param python_version str: the current major python version
    """
    def __init__(self, python_version):
        self.python_version = python_version
        self.set_chrome_path()
        self.messenger = Messenger(self.python_version)
        self.socket_server = Server()
        self.is_running = False

    def set_chrome_path(self):
        """Tries to set the path to the chrome directory."""
        self.chrome_path = get_firefox_chrome_path()

    def check_chrome_path(self, action, target):
        """
        Checks if the path to the 'chrome' directory was found and sends a message if it was not.

        :param action str: the message action
        :param target str: the target CSS file
        :return: if chrome_path is set
        :rType: bool
        """
        if not self.chrome_path:
            self.messenger.send_message(Message(
                action,
                data=target,
                success=False,
                message='Could not find path to chrome folder',
            ))
            return False
        
        return True

    def check_target(self, message):
        """
        Checks if the message received specifies a target, or the message is invalid.

        :param message object: the decoded message
        :return: if message has key 'target' with a valid value
        :rType: bool
        """
        if 'target' in message and len(message['target']) > 0:
            return message['target']

        logging.error('%s: target was not specified' % message['action'])
        self.send_invalid_action()
        return False

    def send_version(self):
        """Sends the current daemon version to the extension."""
        self.messenger.send_message(Message(ACTIONS['VERSION'], data=DAEMON_VERSION))

    def send_pywal_colors(self):
        """Sends the current colorscheme to the extension."""
        (success, colors, message) = get_pywal_colors()
        self.messenger.send_message(Message(
            ACTIONS['COLORS'], 
            data=colors, 
            success=success,
            message=message,
        ))

    def send_invalid_action(self):
        """Sends an action to the extension indicating that the action sent was invalid"""
        self.messenger.send_message(Message(ACTIONS['INVALID_ACTION'], success=False))

    def send_output(self, message):
        """
        Sends an output message to the extension that will be displayed in the 'Debugging output' area.

        :param message str: the message to send to the extension
        """
        self.messenger.send_message(Message(ACTIONS['OUTPUT'], data=message))

    def send_enable_css_response(self, message):
        """
        Tries to enable a custom CSS file and sends the result to the extension.

        :param message string: the name of the CSS file to enable/disable
        """
        action = ACTIONS['CSS_ENABLE']
        target = self.check_target(message)
        if target is not False:
            if self.check_chrome_path(action, target):
                (success, message) = enable_custom_css(self.chrome_path, target)
                self.messenger.send_message(Message(
                    action,
                    data=target,
                    success=success,
                    message=message,
                ))

    def send_disable_css_response(self, message):
        """
        Tries to disable a custom CSS file and sends the result to the extension.

        :param message string: the name of the CSS file to enable/disable
        """
        action = ACTIONS['CSS_DISABLE']
        target = self.check_target(message)
        if target is not False:
            if self.check_chrome_path(action, target):
                (success, message) = disable_custom_css(self.chrome_path, target)
                self.messenger.send_message(Message(
                    action,
                    data=target,
                    success=success,
                    message=message,
                ))

    def send_font_size_response(self, message):
        """
        Tries to set a custom font size in a CSS file.

        :param message string: the name of the CSS file to change the font size in
        """
        action = ACTIONS['CSS_FONT_SIZE']
        target = self.check_target(message)
        if target is not False:
            if self.check_chrome_path(action, target):
                if 'size' in message:
                    new_size = message['size']
                    (success, message) = set_font_size(self.chrome_path, target, new_size)
                    self.messenger.send_message(Message(
                        action,
                        data=new_size,
                        success=success,
                        message=message,
                    ))

    def handle_message(self, message):
        """
        Handles the incoming messages and does the appropriate action.

        :param message object: the decoded message
        """
        try:
            action = message['action']
            if action == ACTIONS['VERSION']:
                self.send_version()
            elif action == ACTIONS['COLORS']:
                self.send_pywal_colors()
            elif action == ACTIONS['CSS_ENABLE']:
                self.send_enable_css_response(message)
            elif action == ACTIONS['CSS_DISABLE']:
                self.send_disable_css_response(message)
            elif action == ACTIONS['CSS_FONT_SIZE']:
                self.send_font_size_response(message)
            else:
                logging.debug('%s: no such action' % action)
                self.send_invalid_action()
        except KeyError:
            logging.error('action was not defined')
            self.send_invalid_action()

    def socket_thread_worker(self):
        """The socket server thread worker."""
        while True:
            message = self.socket_server.get_message()
            if message == 'update':
                logging.debug('Update triggered from external script')
                self.send_pywal_colors()

    def start_socket_server(self):
        """Starts the socket server and creates the socket thread."""
        success = self.socket_server.start()
        if success == True:
            if self.python_version == 3:
                self.socket_thread = Thread(target=self.socket_thread_worker, daemon=True)
            else:
                self.socket_thread = Thread(target=self.socket_thread_worker)

            self.socket_thread.start()

    def start(self):
        """Starts the daemon and listens for incoming messages."""
        self.is_running = True
        self.start_socket_server()
        try:
            while True:
                message = self.messenger.get_message()
                logging.debug('Received message from extension: %s' % message)
                self.handle_message(message)
        except KeyboardInterrupt:
            return

    def close(self):
        """Application cleanup."""
        self.socket_server.close()
        self.is_running = False
        logging.debug('Cleanup')










