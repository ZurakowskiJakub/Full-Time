"""
Get all available leagues
"""

from pprint import pprint

import requests

from src.data.endpoints import Endpoints
from src.database.mongo import Mongo
from src.util.util import get_logger

logger = get_logger(__name__)
ep = Endpoints()
db = Mongo('data_test')


def update_leagues():
    # Get league data from API
    ## resp = requests.get(ep.leagues, headers=ep.headers)
    url = ep.leagues
    resp = ep.get(url)

    # Select only all TIER_ONE leagues -- others we have no data for
    leagues: list = resp.json()['competitions']
    leagues = [league for league in leagues if league['plan'] == 'TIER_ONE']

    # Select desired database location
    collection = db.get_collection('leagues')

    # Remove all
    logger.debug("Removing all leagues...")
    collection.delete_many({})
    logger.debug("Removing all leagues... DONE")

    # Insert all
    logger.debug(
        f"Inserting all leagues... ({len(leagues)} records)")
    collection.insert_many(leagues)
    logger.debug("Inserting all leagues... DONE")

    logger.info("Leagues updated")
