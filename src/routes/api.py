import json

from bson import json_util
from flask import Blueprint, jsonify

from src.database.mongo import Mongo
from src.database.util import doc_to_dict

api_module = Blueprint('api', __name__, url_prefix='/api')
db = Mongo()


@api_module.route('/')
def api_index():
    return jsonify({"let's pretend this is json": "yes"})


@api_module.route('/getAllUsers')
def get_all_users():
    coll = db.get_collection('users')
    documents = coll.find()

    jDocs = []
    for doc in documents:
        jDocs.append(doc_to_dict(doc))
    return jsonify(jDocs)


@api_module.route('/getAllMatches')
def get_all_matches():
    coll = db.get_collection('matches')
    documents = coll.find()

    jDocs = []
    for doc in documents:
        jDocs.append(doc_to_dict(doc))
    return jsonify(jDocs)


@api_module.route('/getMatchInUser')
def get_match_in_user():
    users = db.get_collection('users')
    document = users.find_one()

    matches = db.get_collection('matches')
    document = matches.find_one(
        {'_id': document['predictions'][0]['match_id']})

    return jsonify(
        doc_to_dict(
            document
        )
    )


@api_module.route('/getUserFull')
def get_user_full():
    def id(x): return {'_id': x}

    users = db.get_collection('users')
    user = users.find_one()

    # Get all leagues
    leagues = db.get_collection('leagues')
    league_objs = []
    for league_id in user['leagues']:
        league_objs.append(leagues.find_one(id(league_id)))
    user['leagues'] = league_objs

    # Get all matches
    matches = db.get_collection('matches')
    for match in user['predictions']:
        match['match_id'] = matches.find_one(id(match['match_id']))

    # Return final result
    return jsonify(
        doc_to_dict(
            user
        )
    )


@api_module.route('/getAllLeaguesFromStore')
def get_all_leagues_from_store():
    db = Mongo('data_test')
    coll = db.get_collection('leagues')
    docs = [doc for doc in coll.find()]

    return jsonify(
        doc_to_dict(
            docs
        )
    )


@api_module.route('/getAllMatchesFromStore')
def get_all_matches_from_store():
    db = Mongo('data_test')
    coll = db.get_collection('matches')
    docs = [doc for doc in coll.find()]

    return jsonify(
        doc_to_dict(
            docs
        )
    )
