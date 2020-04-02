import logging
from logging.handlers import RotatingFileHandler

from ..config import *

def create_rotating_log(name, log_level):
    """
    Creates a rotating log which will limit the size of the log file.

    :param name str: the name of the logger to add the rotating log handler to
    :param log_level int: the logging level to use, e.g logging.DEBUG
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=LOG_FILE_FORMAT, datefmt=LOG_FILE_DATE_FORMAT)
    handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=LOG_FILE_MAX_SIZE, backupCount=LOG_FILE_COUNT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def setup_logging(verbose, print_mode):
    """
    Creates a rotating log.

    :param verbose bool: if debug messages should be saved/printed
    :param print_mode bool: whether or not to print to the terminal
    """
    if verbose == True:
        if print_mode == True:
            logging.basicConfig(
                format=LOG_FILE_FORMAT,
                datefmt=LOG_FILE_DATE_FORMAT,
                level=logging.DEBUG
            )
        else:
            logging.basicConfig(
                format=LOG_FILE_FORMAT,
                datefmt=LOG_FILE_DATE_FORMAT,
                filename=LOG_FILE_PATH,
                level=logging.DEBUG,
                filemode='w' # since we are debugging we want to overwrite the log each time
            )
    else:
        create_rotating_log('', logging.ERROR) # use the root logger

