"""Custom logger with colorized output.

MODULE_NAME: LINE_NUMBER: LOG_LEVEL: LOG_MESSAGE

Usage
======

from common.logger import logger

logger.debug(f"{__name__}: This is a debug message.")
logger.info(f"{__name__}: This is an info message.")
logger.warning(f"{__name__}: This is a warning message.")
logger.error(f"{__name__}: This is an error message.")
logger.critical(f"{__name__}: This is a critical message.")

"""


import logging
import os

from dotenv import load_dotenv

# Avoids the overhead of loading the django settings here and
# and loads the environment variables directly.
load_dotenv(".env")

# Verbose log during development but keeping it minimal on production.
if os.environ.get("DEBUG") == "True":
    LOG_LEVEL = logging.INFO
else:
    LOG_LEVEL = logging.ERROR


class BaseFormatter(logging.Formatter):
    """Custom logging formatter to add color. If you wish to change
    the log format, you can subclass `BaseFormatter` and override the
    `.format()` method."""

    CYAN = "\x1b[0;36m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    RESET = "\x1b[0m"
    format = "%(module)s: %(lineno)2d: %(levelname)2s: %(message)s"

    # F-string over string concat & join for readability & performance.
    FORMATS = {
        logging.DEBUG: f"{CYAN}{format}{RESET}",
        logging.INFO: f"{CYAN}{format}{RESET}",
        logging.WARNING: f"{YELLOW}{format}{RESET}",
        logging.ERROR: f"{RED}{format}{RESET}",
        logging.CRITICAL: f"{RED}{format}{RESET}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Creates the logger instance.
logger = logging.getLogger(__name__)

# Stop duplicated logging in the Celery workers. See -
# https://stackoverflow.com/a/45342824/8963300
logger.propagate = False

# Sets the lowest log level.
logger.setLevel(LOG_LEVEL)

# Creates console handler with a higher log level.
ch = logging.StreamHandler()

# Sets the log formatter.
ch.setFormatter(BaseFormatter())

# Adds console handler to the logger instance.
logger.addHandler(ch)
