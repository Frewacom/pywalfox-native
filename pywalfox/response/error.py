import logging

class ErrorMessage:
    """
    Defines the structure of an error message.

    :param action str: the action called by the addon
    :param message str: the error message
    """
    def __init__(self, action, message):
        self.action = action
        self.error = message
        logging.error(message)

    def getMessage(self):
        """Creates the response error message."""
        return {
            'action': self.action,
            'success': False,
            'message': self.message
        }

