import sys
import logging

import config
import fetcher
import custom_css

from response import Message
from messenger import Messenger

class Daemon:
    """
    Application entry point. Initializes the application.

    :param debug bool: if debugging is enabled (defaults to True)
    """
    def __init__(self, debug=False):
        self.debug = debug
        self.setup_logging()
        self.set_chrome_path()
        self.messenger = Messenger()

    def set_chrome_path(self):
        """Tries to set the path to the chrome directory."""
        self.chrome_path = custom_css.get_firefox_chrome_path()
        if not self.chrome_path:
            logging.error('Could not find Firefox profile directory')
        else:
            logging.debug('Found valid chrome directory path')

    def setup_logging(self):
        """Setup logging format and destination."""
        log_level = logging.ERROR
        if self.debug == True:
            log_level = logging.DEBUG

        logging.basicConfig(
            format='[%(asctime)s] %(levelname)s:%(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename=LOG_FILE,
            level=log_level
        )

    def check_chrome_path(self, action):
        """
        Checks if the path to the 'chrome' directory was found and sends a message if it was not.

        :return: if chrome_path is set
        :rType: bool
        """
        if not self.chrome_path:
            this.messenger.send_message(Message(
                config.ACTIONS['custom_css_apply'],
                'Could not find path to chrome folder',
                success=False
            ))
            return False
        else:
            return True

    def send_version(self):
        """Sends the current daemon version to the addon."""
        self.messenger.send_message(Message(config.ACTIONS['version'], config.DAEMON_VERSION))

    def send_colorscheme(self):
        """Sends the current colorscheme to the addon."""
        (success, data) = fetcher.get_colorscheme(config.PYWAL_COLORS_PATH, config.BG_LIGHT_MODIFIER)
        if success == True:
            logging.debug('Successfully fetched pywal colors')
        else:
            logging.error(data)

        this.messenger.send_message(Message(config.ACTIONS['colors'], data, success=success))

    def send_invalid_action(self):
        """Sends an action to the addon indicating that the action sent was invalid"""
        this.messenger.send_message(Message(config.ACTIONS['invalid_action'], {}, success=False))

    def send_output(self, message):
        """
        Sends an output message to the addon that will be displayed in the 'Debugging output' area.

        :param message str: the message to send to the addon
        """
        this.messenger.send_message(Message(config.ACTIONS['output'], message))

    def send_enable_css_response(self, target)
        """
        Tries to enable a custom CSS file and sends the result to the addon.

        :param target string: the name of the CSS file to enable/disable
        """
        action = config.ACTIONS['custom_css_enable']
        if self.check_chrome_path(action):
            (success, message) = custom_css.enable_custom_css(self.chrome_path, target)
            this.messenger.send_message(Message(action, message, success=success))

    def send_disable_css_response(self, target):
        """
        Tries to disable a custom CSS file and sends the result to the addon.

        :param target string: the name of the CSS file to enable/disable
        """
        action = config.ACTIONS['custom_css_disable']
        if self.check_chrome_path(action):
            (success, message) = custom_css.disable_custom_css(self.chrome_path, target)
            this.messenger.send_message(Message(action, message, success=success))









