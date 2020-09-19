import logging

from flask import Flask

from src.config.config import Config
from src.data.scheduler import run_scheduler
from src.database.firebase import init_firebase
from src.routes.api import api_module
from src.routes.app import app_module
# from src.routes.auth import auth_module
from src.util.util import get_logger

config = Config()

logger = get_logger(__name__)

app = Flask(__name__)

app.config.from_object('src.config.config.Config')
app.secret_key = config.SECRET_KEY

app.register_blueprint(app_module)
# app.register_blueprint(auth_module)
app.register_blueprint(api_module)

init_firebase()

# Run Scheduler
# if config.ENV != 'Development':
# run_scheduler()

if __name__ == "__main__":
    logger.debug("App starting with debug=True")
    app.run(host='127.0.0.1', port=8080)
