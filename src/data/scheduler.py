import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from src.data.leagues import update_leagues
from src.data.matches import update_matches
from src.util.util import get_logger

logger = get_logger(__name__, file_name="scheduler.log")

jobs = [
    {
        'name': 'leagues',
        'func': update_leagues,
        'min': 60
    },
    {
        'name': 'matches',
        'func': update_matches,
        'min': 10
    },
]


def main():
    scheduler = BackgroundScheduler()

    for job in jobs:
        scheduler.add_job(func=job['func'],
                          trigger='interval', minutes=job['min'])
        logger.info(f"Registered job: {job['name']}")

    scheduler.start()

    # Close Scheduler on Exit
    atexit.register(lambda: scheduler.shutdown())


def run_scheduler():
    main()
