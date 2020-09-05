import os

from dotenv import load_dotenv


class Config(object):
    "General Configuration - Takes variables from .env"

    def __init__(self):
        """Constructor. Performs checks on .env variables

        :raises ValueError: If any of the .env variables are not set
        """

        load_dotenv()

        expected_env_vars = {
            'FLASK_DEBUG',
            'FLASK_TESTING',
            'FLASK_SECRET_KEY',
            'FLASK_ENV',
            'MONGO_URI',
            'LOGGING_LEVEL'
        }

        for expected in expected_env_vars:
            if not os.getenv(expected):
                raise ValueError(f"No {expected} set for this application.")

        self.ENV = os.getenv("FLASK_ENV")
        self.DEBUG = True if os.getenv("FLASK_DEBUG") == 'True' else False
        self.TESTING = True if os.getenv("FLASK_TESTING") == 'True' else False
        self.SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
        self.MONGO_URI = os.getenv("MONGO_URI")

        # Read logging level - defaults to INFO (20)
        logging_vals = [0, 10, 20, 30, 40, 50]
        LOGGING_LEVEL = int(os.getenv("LOGGING_LEVEL"))
        if LOGGING_LEVEL in logging_vals:
            self.LOGGING_LEVEL = LOGGING_LEVEL
        else:
            self.LOGGING_LEVEL = 20
