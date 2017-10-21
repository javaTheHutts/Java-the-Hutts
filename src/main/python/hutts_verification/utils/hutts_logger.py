"""
Wraps the logic required to setup and use a custom logger while
disabling the built-in flask logger.

Example usage:

First import the logger from the hutts_logger module...
from hutts_verification.utils.hutts_logger import logger
then start logging.

``logger.info('logging an example')``

There are 5 logging levels, as shown below with their corresponding
function call (from lowest to highest level):

    - DEBUG       -   ``logger.debug(message)``
    - INFO        -   ``logger.info(message)``
    - WARNING     -   ``logger.warning(message)``
    - ERROR       -   ``logger.error(message)``
    - CRITICAL    -   ``logger.critical(message)``

The default level of the logger will be INFO, unless the flask app is
run in debug mode, in which case the logger level will be DEBUG.
What this means is that messages lower than INFO, i.e. DEBUG, will
not be shown, again this is unless the flask app is run in debug
mode.

.. note:    A function (prettify_json_message) has been included to take
            a json obj/dict and return a prettified string of said json obj/dict
            in the event that someone wishes to display a message in the form of
            a json obj/dict.

"""

import colorlog
import errno
import json
import logging
import os
from logging.handlers import RotatingFileHandler

__author__ = "Jan-Justin van Tonder"
__copyright__ = "Copyright 2017, Java the Hutts"
__license__ = "BSD"
__maintainer__ = "Jan-Justin van Tonder"
__email__ = "J.vanTonder@tuks.co.za"
__status__ = "Development"

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
For a more detailed description see the colorlog documentation: https://github.com/borntyping/python-colorlog.
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
For a more detailed description see the colorlog documentation: https://github.com/borntyping/python-colorlog.
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
"""Specifies the maximum number of bytes for the log file before a rotate (assuming a rotating file is used)."""
LOGGING_LOG_TO_FILE_MAX_BYTES = 100000
"""Specifies the number of backups for the log file (assuming a rotating file is used)."""
LOGGING_LOG_TO_FILE_BACKUP_COUNT = 1
"""Specifies the encoding for the log file."""
LOGGING_LOG_TO_FILE_ENCODING = 'utf8'

"""
A global reference to the custom logger to be used.
It is initialised to the default python logger to avoid errors during installation of packages.
"""
logger = None


def setup_logger():
    """
    This function is responsible for creating the custom logger and delegating the creation of its handlers.
    """
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(LOGGING_DEFAULT_LEVEL)
    if LOGGING_LOG_TO_CONSOLE:
        console_handler = get_console_handler()
        console_handler.setLevel(LOGGING_DEFAULT_LEVEL)
        logger.addHandler(console_handler)
    if LOGGING_LOG_TO_FILE:
        file_handler = get_file_handler(LOGGING_LOG_TO_FILE_DEFAULT_DIR)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)


def disable_flask_logging(app_instance):
    """
    This function disables the flask logging, which interferes with the custom logger.

    :param app_instance (obj): A reference to the current flask server application.

    """
    app_instance.handlers = []
    app_instance.logger.propagate = False
    logging.getLogger('werkzeug').disabled = True


def get_console_handler():
    """
    This function is responsible for creating a console log handler with a global format and returning it.

    Returns:
        - (obj): A log handler that is responsible for logging to the console.

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
        - (obj): A log handler that is responsible for logging to a file.

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
    handler = RotatingFileHandler(
        log_file_path,
        encoding=LOGGING_LOG_TO_FILE_ENCODING,
        maxBytes=LOGGING_LOG_TO_FILE_MAX_BYTES,
        backupCount=LOGGING_LOG_TO_FILE_BACKUP_COUNT
    )
    handler.setFormatter(formatter)
    return handler


def prettify_json_message(json_message):
    """
    This function is a helper function that is used to prettify a json/dict message obj so that is more readable
    for humans when it is logged.

    :param json_message (dict): A message that is to be prettified before being logged.

    Returns:
        - (str): A prettified json message string.

    """
    return json.dumps(json_message, indent=2, sort_keys=True)


# Set up the logger.
setup_logger()
