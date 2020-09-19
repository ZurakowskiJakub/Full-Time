import firebase_admin
from firebase_admin import credentials

from src.config.config import Config

config = Config()


def init_firebase():
    cred = credentials.Certificate(config.FIREBASE_JSON)
    firebase_admin.initialize_app(cred)
