import sys
import logging

import config
import fetcher

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
        self.messenger = Messenger()

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







