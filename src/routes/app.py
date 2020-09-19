from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request, session

from src.config.config import Config
from src.database.mongo import Mongo
from src.model.User import User
from src.util.util import json_err

app_module = Blueprint('app', __name__)

db = Mongo()

config = Config()


@app_module.before_app_request
def before_every_request():
    user_id = request.form.get('user_id', None)
    if not user_id:
        return json_err("user_id missing.")

    # Check if auth should be disabled
    disable_auth = config.DISABLE_AUTH

    # Check if user in session already
    session_expiry = session.get('user_exp', None)
    session_user = session.get('user_id', None)

    if (session_expiry and session_expiry <= datetime.now()) or user_id != session_user:
        if disable_auth:
            # user = User.authenticate('abcd')
            # user = User('5f627af0f6939c29ed2e2995')
            auth_resp = User('5f627af0f6939c29ed2e2995')
        else:
            auth_resp = User.authenticate(user_id, 'testing_user')

        if isinstance(auth_resp, tuple):
            # If tuple, it's an error message
            return auth_resp
        else:
            # Else it's a user object
            user = auth_resp

        session['user_exp'] = datetime.now() + timedelta(hours=2)
        session['user_id'] = str(user._id)


@app_module.after_app_request
def after_every_request(response):
    # TODO
    return response
