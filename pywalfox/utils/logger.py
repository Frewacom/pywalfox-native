import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE, LOG_FILE_COUNT, LOG_FILE_MAX_SIZE

def create_rotating_log(name, log_level, log_format, log_datefmt):
    """
    Creates a rotating log which will limit the size of the log file.

    :param name str: the name of the logger to add the rotating log handler to
    :param log_level int: the logging level to use, e.g logging.DEBUG
    :param log_format str: the format of each log message
    :param log_datefmt str: the format of the timestamp
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=log_format, datefmt=log_datefmt)
    handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_FILE_MAX_SIZE, backupCount=LOG_FILE_COUNT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def setup_logging(verbose, print_mode):
    """
    Creates a rotating log.

    :param verbose bool: if debug messages should be saved/printed
    :param print_mode bool: whether or not to print to the terminal
    """
    log_format = '[%(asctime)s] %(levelname)s:%(message)s'
    log_datefmt = '%m-%d-%Y %I:%M:%S'

    if verbose == True:
        if print_mode == True:
            logging.basicConfig(
                format=log_format,
                datefmt=log_datefmt,
                level=logging.DEBUG
            )
        else:
            logging.basicConfig(
                format=log_format,
                datefmt=log_datefmt,
                filename=LOG_FILE,
                level=logging.DEBUG,
                filemode='w' # since we are debugging we want to overwrite the log each time
            )
    else:
        create_rotating_log('', logging.ERROR, log_format, log_datefmt) # use the root logger

