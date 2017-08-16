"""
----------------------------------------------------------------------
Author: Jan-Justin van Tonder
----------------------------------------------------------------------
Wraps the logic required to setup and use the flask logging for
debugging and production.
----------------------------------------------------------------------
"""
import colorlog
import errno
import json
import logging
import os
from logging.handlers import RotatingFileHandler

"""Specifies the name of the custom logger."""
LOGGING_LOGGER_NAME = 'hutts_logger'
"""Specifies the default level for logging."""
LOGGING_DEFAULT_LEVEL = logging.DEBUG
"""Specifies the date format to be used by the various logging formatters."""
LOGGING_LOG_DATE_FMT = '%Y-%m-%d %H:%M:%S'

"""Indicates whether or not to log to console."""
LOGGING_LOG_TO_CONSOLE = True
"""Specifies the log format to be used when logging to the console."""
LOGGING_LOG_TO_CONSOLE_FMT = '[%(asctime)s.%(msecs)03d]%(log_color)s[%(levelname)8s]%(reset)s%(message_log_color)s ' \
                             '-- (%(filename)s:%(lineno)d) -- %(message)s'
"""
Specifies the colours to be used to indicate the different levels when logging to console.
For a more detailed description see the colorlog documentation: https://github.com/borntyping/python-colorlog
"""
LOGGING_LOG_TO_CONSOLE_COLOURS = {
    'DEBUG':    'bold_cyan',
    'INFO':     'bold_white',
    'WARNING':  'bold_yellow',
    'ERROR':    'bold_red',
    'CRITICAL': 'bold_red,bg_white',
}
"""
Specifies the secondary colours to be used to indicate the different levels when logging to console.
For a more detailed description see the colorlog documentation: https://github.com/borntyping/python-colorlog
"""
LOGGING_LOG_TO_CONSOLE_SEC_COLOURS = {
    'message': {
        'ERROR':    'red',
        'CRITICAL': 'bold_red,bg_white',
    }
}

"""Indicates whether or not to log to a file."""
LOGGING_LOG_TO_FILE = True
"""Specifies the name of the log file."""
LOGGING_LOG_TO_FILE_FILENAME = 'hutts_verification.log'
"""Specifies the default directory for the log file in the event that one is not specified during setup."""
LOGGING_LOG_TO_FILE_DEFAULT_DIR = 'log/'
"""Specifies the log format to be used when logging to a file."""
LOGGING_LOG_TO_FILE_FMT = '[%(asctime)s.%(msecs)03d][%(levelname)8s] -- (%(filename)s:%(lineno)d) -- %(message)s'

"""
A global reference to the custom logger to be used.
It is initialised to the default python logger to avoid errors during installation of packages.
"""
logger = logging


def setup_logger(log_file_dir=None):
    """
    This function is responsible for creating the custom logger and delegating the creation of its handlers.

    Author:
        Jan-Justin van Tonder

    Args:
        log_file_dir (str): A directory in which the logger is to log to a file.
    """
    global logger
    logger = logging.getLogger(LOGGING_LOGGER_NAME)
    logger.setLevel(LOGGING_DEFAULT_LEVEL)
    if LOGGING_LOG_TO_CONSOLE:
        console_handler = get_console_handler()
        logger.addHandler(console_handler)
    if LOGGING_LOG_TO_FILE:
        file_handler = get_file_handler(log_file_dir)
        logger.addHandler(file_handler)


def disable_flask_logging(app):
    """
    This function disables the flask logging, which interferes with the custom logger.

    Author:
        Jan-Justin van Tonder

    Args:
        app (obj): A reference to the current flask server application.
    """
    app.logger.handlers = []
    app.logger.propagate = True
    logger.getLogger('werkzeug').disabled = True


def get_console_handler():
    """
    This function is responsible for creating a console log handler with a global format and returning it.

    Returns:
        handler (obj): A log handler that is responsible for logging to the console.
    """
    formatter = colorlog.ColoredFormatter(
        fmt=LOGGING_LOG_TO_CONSOLE_FMT,
        datefmt=LOGGING_LOG_DATE_FMT,
        log_colors=LOGGING_LOG_TO_CONSOLE_COLOURS,
        secondary_log_colors=LOGGING_LOG_TO_CONSOLE_SEC_COLOURS
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    return handler


def get_file_handler(log_dir=None):
    """
    This function is responsible for creating a file log handler with a global format and returning it.

    Returns:
        handler (obj): A log handler that is responsible for logging to a file.
    """
    log_file_dir = log_dir if log_dir else LOGGING_LOG_TO_FILE_DEFAULT_DIR
    try:
        if not os.path.exists(log_file_dir):
            os.makedirs(log_file_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    log_file_path = os.path.join(log_file_dir, LOGGING_LOG_TO_FILE_FILENAME)
    formatter = logging.Formatter(fmt=LOGGING_LOG_TO_FILE_FMT, datefmt=LOGGING_LOG_DATE_FMT)
    handler = RotatingFileHandler(log_file_path, encoding='utf8', maxBytes=100000, backupCount=1)
    handler.setFormatter(formatter)
    return handler


def prettify_json_message(json_message):
    """
    This function is a helper function that is used to prettify a json/dict message string so that is more readable
    for humans when it is logged.

    Args:
        json_message (dict): A message that is to be prettified before being logged.

    Returns:
        (str): A prettified json message string.
    """
    return json.dumps(json_message, indent=2, sort_keys=True)
