# Description: This script defines a simple logging utility that creates
# a logger with a specified name and log level, and outputs log messages
# to the console and log file.

import logging
import sys
import os


def get_logger(name: str, level: int = 20) -> logging.Logger:
    """
    Simple logging utility that creates a logger with a specified name
    and log level, and outputs log messages to the console or if the
    level is set to DEBUG a log file is created.
    The log file is created in the same directory as the script, with the
    name of the logger as the file name.
    Args:
        name (str): The name of the logger.
        level (int): The log level (default is INFO).
    Returns:
        logging.Logger: The configured logger.
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
            '| Name: %(name)s ' +
            '| Level: %(levelname)s ' +
            '| Process: %(process)d ' +
            '| Path: %(pathname)s ' +
            '| File: %(filename)s ' +
            '| Module: %(module)s  ' +
            '| Funcion: %(funcName)s ' +
            '| Line: %(lineno)d ' +
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

    if level == logging.DEBUG:
        # Create the handlers
        file_handler = logging.FileHandler(file_path)
        # Add the formatter to the handlers
        file_handler.setFormatter(formatter)
        # Add the handlers to the logger
        logger.addHandler(file_handler)
    else:
        # Create the handler
        consol_handler = logging.StreamHandler(sys.stdout)
        # Add the formatter to the handler
        consol_handler.setFormatter(formatter)
        # Add the handlers to the logger
        logger.addHandler(consol_handler)
    return logger


if __name__ == "__main__":
    debug_logger = get_logger("debug", logging.DEBUG)
    debug_logger.debug("This is a debug message")
    debug_logger.info("This is an info message")
    debug_logger.warning("This is a warning message")
    debug_logger.error("This is an error message")
    debug_logger.critical("This is a critical message")

    logger = get_logger("default")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

# Output:

# 2025-05-01 10:18:04,233 | Name: debug | Level: DEBUG | Process: 83175 | Path: /Users/andrew/Documents/_Development_Learning/Programming/Python/100-Days-of-Code-Python/day0091_Professional_Portfolio_Project-Python_HTTP_Request-API-PDF_to_Audiobook/pdf-to-speech/modules/logger.py | File: logger.py | Module: logger  | Funcion: <module> | Line: 70 | This is a debug message
# 2025-05-01 10:18:04,233 | Name: debug | Level: INFO | Process: 83175 | Path: /Users/andrew/Documents/_Development_Learning/Programming/Python/100-Days-of-Code-Python/day0091_Professional_Portfolio_Project-Python_HTTP_Request-API-PDF_to_Audiobook/pdf-to-speech/modules/logger.py | File: logger.py | Module: logger  | Funcion: <module> | Line: 71 | This is an info message
# 2025-05-01 10:18:04,233 | Name: debug | Level: WARNING | Process: 83175 | Path: /Users/andrew/Documents/_Development_Learning/Programming/Python/100-Days-of-Code-Python/day0091_Professional_Portfolio_Project-Python_HTTP_Request-API-PDF_to_Audiobook/pdf-to-speech/modules/logger.py | File: logger.py | Module: logger  | Funcion: <module> | Line: 72 | This is a warning message
# 2025-05-01 10:18:04,233 | Name: debug | Level: ERROR | Process: 83175 | Path: /Users/andrew/Documents/_Development_Learning/Programming/Python/100-Days-of-Code-Python/day0091_Professional_Portfolio_Project-Python_HTTP_Request-API-PDF_to_Audiobook/pdf-to-speech/modules/logger.py | File: logger.py | Module: logger  | Funcion: <module> | Line: 73 | This is an error message
# 2025-05-01 10:18:04,233 | Name: debug | Level: CRITICAL | Process: 83175 | Path: /Users/andrew/Documents/_Development_Learning/Programming/Python/100-Days-of-Code-Python/day0091_Professional_Portfolio_Project-Python_HTTP_Request-API-PDF_to_Audiobook/pdf-to-speech/modules/logger.py | File: logger.py | Module: logger  | Funcion: <module> | Line: 74 | This is a critical message

# | This is an info message
# | This is a warning message
# | This is an error message
# | This is a critical message


# This logger can be used in other modules by importing the get_logger
# function and calling it with a unique name for each module. This allows
# for better organization and customization of log messages in a multi-module
# application.
