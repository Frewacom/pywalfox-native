import logging

class Message:
    """
    Defines the structure of a generic message.

    :param action str: the action called by the addon
    :param message str: the success message
    :param data any: the additional data to send along with the message
    """
    def __init__(self, action, message, data):
       self.action = action
       self.message = message
       self.data = data

       logging.debug(message)

    def getMessage(self):
        """Creates the response message."""
        return {
            'action': self.action,
            'success': True,
            'message': self.message,
            'data': self.data
        }

