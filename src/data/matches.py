"""
Get all available matches for given day
"""

import time
from pprint import pprint

import requests

from src.data.endpoints import Endpoints
from src.database.mongo import Mongo
from src.util.util import get_logger

logger = get_logger(__name__)
ep = Endpoints()
db = Mongo('data_test')


def update_matches():
    matches = []

    # Get all Leagues
    leagues = db.get_collection('leagues')

    # Loop over every league, getting matches for most-recent season.
    for league in leagues.find():
        # TODO url = ep.url(f"competitions/{league['id']}/matches")
        url = ep.matches(league['id'])
        # TODO resp = requests.get(url, headers=ep.headers)
        resp = ep.get(url)

        # If out of requests, wait till we have more
        # if resp.status_code == 429:
        #     seconds = int(resp.json()['message'].split(' ')[-2]) + 5

        #     logger.warning(
        #         f"Max requests reached. Sleeping for {seconds} sec...")
        #     time.sleep(seconds)

        #     # TODO resp = requests.get(url, headers=ep.headers)
        #     resp = ep.get(url)

        # Add matches to a List
        if not resp.json().get('matches'):
            logger.error(str(resp.json()))
        matches_json = resp.json()['matches']

        for match in matches_json:
            match['league'] = league['_id']

        matches.extend(matches_json)

    # Select desired database location
    collection = db.get_collection('matches')

    # TODO We should loop through each match, and update it in the DB.

    # Remove all
    logger.debug("Removing all matches...")
    no_deleted = collection.delete_many({})
    logger.debug(f"Removing all matches... ({no_deleted.deleted_count}) DONE")

    # Insert all
    logger.debug(
        f"Inserting all matches... ({len(matches)} records)")
    collection.insert_many(matches)
    logger.debug("Inserting all matches... DONE")

    logger.info("Matches updated")
