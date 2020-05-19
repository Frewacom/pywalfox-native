import os
import logging

from .config import PYWAL_COLORS_PATH

def get_colorscheme():
    """
    Fetches the pywal colors from the cache file.

    :return: the colors generated by pywal
    :rType: list
    """
    colors = []
    try:
        with open(PYWAL_COLORS_PATH, 'r') as f:
            for line in f.readlines():
                colors.append(line.rstrip('\n'))
    except IOError:
        error_message = 'Could not read colors from: %s' % PYWAL_COLORS_PATH
        logging.error(error_message)
        return (False, error_message)

    if len(colors) < 16:
        error_message = '%s containing the generated pywal colors is invalid' % PYWAL_COLORS_PATH
        logging.error(error_message)
        return (False, error_message)

    logging.debug('Successfully fetched pywal colors and created colorscheme')
    return (True, colors)
