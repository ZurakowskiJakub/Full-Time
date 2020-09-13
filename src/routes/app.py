from flask import Blueprint, jsonify, request

from src.database.mongo import Mongo

app_module = Blueprint('app', __name__)

db = Mongo()


@app_module.before_app_request
def before_every_request():
    # TODO
    pass


@app_module.after_app_request
def after_every_request(response):
    # TODO
    return response


@app_module.route('/')
def app_index():
    return jsonify({"Hello": "World"})


@app_module.route('/getDatabases')
def get_databases():
    return jsonify(db._client.database_names())


@app_module.route('/getCollections')
def get_collections():
    return jsonify(db._db.collection_names())
