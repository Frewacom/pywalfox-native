import logging

class Message:
    """
    Defines the structure of a generic message.

    :param action str: the action called by the extension
    :param data any: the additional data to send along with the message
    :param success bool: if the action was successfull
    :param error str: the error message if success is False
    """
    def __init__(self, action, data=None, success=True, message=None):
        self.action = action
        self.success = success
        self.data = data
        self.message = message

    def getMessage(self):
        """Creates the response message."""
        message = {
            'action': self.action,
            'success': self.success
        }

        if self.data is not None:
            message['data'] = self.data

        if self.message is not None:
            if self.success is True:
                message['message'] = self.message
            else:
                message['error'] = self.message

        logging.debug('Created message: %s' % message)
        return message
