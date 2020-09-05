from flask import Blueprint, jsonify

from src.database.mongo import Mongo

api_module = Blueprint('api', __name__, url_prefix='/api')


db = Mongo()


@api_module.route('/')
def api_index():
    return jsonify({"let's pretend this is json": "yes"})
