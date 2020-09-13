"""
Endpoints for https://www.football-data.org/
"""

import time

import requests

from src.config.config import Config
from src.util.util import get_logger

config = Config()
logger = get_logger(__name__)


class Endpoints():
    # Local vars
    _base_url = "https://api.football-data.org/v2"

    _headers = {
        'X-Auth-Token': config.FOOTBALL_DATA_KEY
    }

    # Endpoints
    leagues = 'competitions'

    def matches(self, id_or_code: str):
        return f"competitions/{id_or_code}/matches"

    # def __init__(self):
    #     self.leagues = self.url('competitions')
    #     self.matches = self.url('matches')

    # Functions
    def url(self, url_path: str) -> str:
        """Create a URL with base https://api.football-data.org/v2/

        :param url_path: The path / endpoint to be used
        :type url_path: str
        :return: The full api endpoint / string
        :rtype: str
        """
        return f"{self._base_url}/{url_path}"

    def get(self, url: str, headers=None) -> requests.Response:
        """Send the request to the API.
        Request-limit safe method. If too many requests, waits for time.

        :param url: The URL following the base api.football-data.org/v2/
        :type url: str
        :param headers: Custom headers, if None uses default
        :type headers: dict, optional
        :return: The Request response
        :rtype: Request
        """
        resp = requests.get(
            self.url(url),
            headers=headers or self._headers
        )

        if resp.status_code == 429:
            # seconds = int(resp.json()['message'].split(' ')[-2]) + 5
            seconds = 65

            logger.warning(
                f"Max requests reached for {url}. Sleeping for {seconds} sec...")
            time.sleep(seconds)

            resp = self.get(url)

        return resp

    def get_json(self, url: str, headers=None) -> dict:
        """Send the request to the API and returns JSON or None.
        Request-limit not-safe method. Can return {error: "..."}.

        :param url: The URL following the base api.football-data.org/v2/
        :type url: str
        :param headers: Custom headers, if None uses default
        :type headers: dict, optional
        :return: The JSON request response
        :rtype: dict
        """
        return requests.get(
            self.url(url),
            headers=headers or self._headers
        ).json() or None
