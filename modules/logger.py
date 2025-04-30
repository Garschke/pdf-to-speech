# Description: This script defines a simple logging utility that creates
# a logger with a specified name and log level, and outputs log messages
# to the console and log file.

import logging
import sys
import os


def get_logger(name: str, level) -> logging.Logger:
    """
    Simple logging utility that creates a logger with a specified name
    and log level, and outputs log messages to the console and log file.
    """
    # get file path for log file, based on current path and logger name
    file_path = os.path.join(os.path.dirname(__file__), name + '.log')
    # Get the logger and set its level
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Create the formatter
    if level == logging.DEBUG:
        formatter = logging.Formatter(
            '%(asctime)s ' +
            # '| Name: %(name)s ' +
            # '| Level: %(levelname)s ' +
            # '| Process: %(process)d ' +
            # '| Path: %(pathname)s ' +
            # '| File: %(filename)s ' +
            '| Module: %(module)s  ' +
            '| Funcion: %(funcName)s ' +
            '| Line: %(lineno)d ' +
            '| %(message)s'
        )
    elif level == logging.INFO:
        formatter = logging.Formatter(
            # '%(asctime)s ' +
            # '| Name: %(name)s ' +
            # '| Level: %(levelname)s ' +
            # '| Process: %(process)d ' +
            # '| Path: %(pathname)s ' +
            # '| File: %(filename)s ' +
            # '| Module: %(module)s  ' +
            # '| Funcion: %(funcName)s ' +
            # '| Line: %(lineno)d ' +
            '| %(message)s'
        )
    else:
        formatter = logging.Formatter(
            # '%(asctime)s ' +
            # '| Name: %(name)s ' +
            # '| Level: %(levelname)s ' +
            # '| Process: %(process)d ' +
            # '| Path: %(pathname)s ' +
            # '| File: %(filename)s ' +
            # '| Module: %(module)s  ' +
            # '| Funcion: %(funcName)s ' +
            # '| Line: %(lineno)d ' +
            '| %(message)s'
        )
    # Create the handlers
    file_handler = logging.FileHandler(file_path)
    consol_handler = logging.StreamHandler(sys.stdout)
    # Add the formatter to the handlers
    file_handler.setFormatter(formatter)
    consol_handler.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(consol_handler)
    return logger


if __name__ == "__main__":
    logger = get_logger("test", logging.DEBUG)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

# Output:
# 2020-07-20 17:03:09,431 - test - DEBUG - This is a debug message
# 2020-07-20 17:03:09,431 - test - INFO - This is an info message
# 2020-07-20 17:03:09,431 - test - WARNING - This is a warning message
# 2020-07-20 17:03:09,431 - test - ERROR - This is an error message
# 2020-07-20 17:03:09,431 - test - CRITICAL - This is a critical message

# This logger can be used in other modules by importing the get_logger
# function and calling it with a unique name for each module. This allows
# for better organization and customization of log messages in a multi-module
# application.
