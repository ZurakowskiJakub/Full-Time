from typing import Union

from bson.objectid import ObjectId
from firebase_admin import auth
from flask.json import jsonify

from src.database.mongo import Mongo
from src.database.util import doc_to_dict
from src.model.UserLeague import UserLeague
from src.util.util import json_err


class User:

    db = Mongo()
    collection = db.get_collection('users')

    def __init__(self, user_id: Union[str, ObjectId]):

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        self._id = user_id

        user = self.collection.find_one({"_id": self._id})

        if not user:
            # Can't find that ID
            raise AttributeError()

        self.firebase_id = user['firebase_id']  # User's Firebase ID
        self.name = user['name']  # User's displayname
        self.predictions = user['predictions']  # User's predictions
        self.user_leagues = user['user_leagues']  # User's user_leagues

    def create_user_league(self, name: str):
        # Create the new User League
        user_league = UserLeague.new(name, self, [])

        # Save changes to DB
        coll = self.collection
        coll.update(
            {'_id': self._id},
            {'$push': {'user_leagues': user_league._id}}
        )

        # Mimick the changes locally
        self.user_leagues.append(user_league._id)

        return user_league

    def update_user_leagues(self, league_id: ObjectId):
        coll = self.collection
        coll.update_one(
            {'_id': self._id},
            {'$push': {'user_leagues': league_id}}
        )

        self.user_leagues.append(league_id)

        return self

    @classmethod
    def new(cls, firebase_id: str, name: str):
        coll = cls.collection

        insert = coll.insert_one({
            "firebase_id": firebase_id,
            "name": name,
            "predictions": [],
            "user_leagues": [],
        })

        return User(insert.inserted_id)

    @classmethod
    def authenticate(cls, firebase_token: str, display_name: str):
        # If user exists, return, if not, create

        try:
            decoded_token = auth.verify_id_token(firebase_token)
        except ValueError:
            return json_err("Bad request.")
        except auth.ExpiredIdTokenError:
            return json_err("User token expired.", 401)
        except auth.InvalidIdTokenError:
            return json_err("Can't authenticate user.", 401)

        firebase_id = decoded_token['uid']
        # TODO get display_name from FIREBASE
        # user_name = auth.get_user(firebase_id)['user_name']
        user_name = display_name

        # SAMPLE USERS
        # firebase_id = 'abcdefghijklmnoprst1234'
        # user_name = 'lomix'
        # firebase_id = '12345678901234567890'
        # user_name = 'Jakub'
        # firebase_id = 'whoCares'
        # user_name = 'Zur'

        coll = cls.collection

        user = coll.find_one({'firebase_id': firebase_id})

        if user:
            return User(user['_id'])
        else:
            return cls.new(firebase_id, user_name)

    def __str__(self):
        return str(self.json())

    def json(self):
        return jsonify(
            doc_to_dict({
                "_id": self._id,
                "firebase_id": self.firebase_id,
                "name": self.name,
                "predictions": self.predictions,
                "user_leagues": self.user_leagues,
            })
        )
