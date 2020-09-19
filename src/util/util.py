import logging

from flask.json import jsonify

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


def get_required_params(request, expected_params: list, type: str = 'POST') -> dict:
    """Gets the list of params from request, or returns None if ANY is missing.

    :param request: The Request
    :type request: flask.Request
    :param expected_params: The list of expected parameters
    :type expected_params: list
    :param type: The request type, defaults to POST, can be GET to get query params.
    :type type: str
    :return: Dictorinary with parameters as keys and values as values
    :rtype: dict
    """

    res = {}
    for param in expected_params:
        if type == 'POST':
            val = request.form.get(param)
        elif type == 'GET':
            val = request.args.get(param)
        else:
            val = None
        if not val:
            return None
        res[param] = val
    return res


def json_err(message: str, status: int = 400) -> tuple:
    """Generate a json error message
    {error: message}, status

    :param message: Error message to be provided
    :type message: str
    :param status: The status to be used, defaults to 400
    :type status: int, optional
    :return: Tuple, jsonified text and status code
    :rtype: tuple
    """

    return jsonify({'error': message}), status


def json_msg(message: str, status: int = 200) -> tuple:
    """Generate a json message
    {message: message}, status

    :param message: Message to be provided
    :type message: str
    :param status: The status to be used, defaults to 200
    :type status: int, optional
    :return: Tuple, jsonified text and status code
    :rtype: tuple
    """

    return jsonify({'message': message}), status
