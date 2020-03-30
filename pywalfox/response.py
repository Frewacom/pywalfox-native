import logging

class Message:
    """
    Defines the structure of a generic message.

    :param action str: the action called by the addon
    :param data any: the additional data to send along with the message
    :param success bool: if the action was successfull
    """
    def __init__(self, action, data, success=True):
        self.action = action
        self.succcess = success
        self.data = data

    def getMessage(self):
        """Creates the response message."""
        message = {
            'action'; self.action,
            'success': self.success
        }

        if self.success == True:
            message['data'] = self.data
        else:
            message['error'] = self.data

        logging.debug('Created message: %s' % message)
        return message
