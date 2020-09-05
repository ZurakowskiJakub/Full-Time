import logging

import pymongo

from src.config.config import Config
from src.util.util import get_logger

logger = get_logger(__name__)


class Mongo():
    """Handler class for MongoDB.
    Connects to the client defined in .env.
    Default database is `dat_main`.
    """

    def __init__(self, db_name: str = 'dat_main'):
        """Constructor for Mongo()

        :param db_name: default database overwrite, defaults to 'dat_main'
        :type db_name: str, optional
        """

        config = Config()

        client = pymongo.MongoClient(config.MONGO_URI)
        logger.info(f"Connected to MongoDB with {config.MONGO_URI}")
        db = client.get_database(db_name)
        logger.info(f"Connected to database {db_name}")

        self._client = client
        self._db = db

    def get_collection(self, collection_name: str):
        """Returns a requested collection

        :param collection_name: name of the requested collection
        :type collection_name: str
        :return: mongoDB Collection
        :rtype: pymongo.Collection
        """

        collection = self._db.get_collection(collection_name)
        logger.debug(
            f"Fetched {collection.name} from database {self._db.name}")

        return collection

    def create_collection(self, collection_name: str):
        """DEPRECATED

        Created and returns the requested collection

        :param collection_name: name of the collection to be created
        :type collection_name: str
        :return: mongoDB Collection
        :rtype: pymongo.Collection
        """

        collection = self._db.create_collection(collection_name)
        logger.debug(
            f"Created {collection.name} collection in database {self._db.name}")

        return collection
