import logging

from src.config.config import Config

config = Config()


def get_logger(name: str):
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

    logging.basicConfig(level=config.LOGGING_LEVEL)

    logger = logging.getLogger(name)

    return logger
