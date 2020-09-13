import logging

from src.config.config import Config

config = Config()

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M.%S"


def get_logger(name: str, file_name=None) -> logging.Logger:
    """Get Logger with proper config

    :param name: The name to use, usually __name__
    :type name: str
    :return: The Logger
    :rtype: Logger
    """

    # if config.ENV.lower() == 'local':
    #     # If local, do not write to file
    #     logging.basicConfig(level=config.LOGGING_LEVEL)
    # else:
    #     # If not local, write to file
    #     logging.basicConfig(filename='main.log', level=config.LOGGING_LEVEL)

    if file_name:
        logging.basicConfig(
            level=config.LOGGING_LEVEL,
            filename=file_name,
            filemode='a'
        )
    else:
        logging.basicConfig(level=config.LOGGING_LEVEL)

    logger = logging.getLogger(name)

    return logger
