from typing import Union

from bson.objectid import ObjectId
from flask.json import jsonify

from src.database.mongo import Mongo
from src.database.util import doc_to_dict


class UserLeague:

    db = Mongo()
    collection = db.get_collection('user_leagues')

    def __init__(self, user_league_id: Union[str, ObjectId]):
        if isinstance(user_league_id, str):
            user_league_id = ObjectId(user_league_id)

        self._id = user_league_id

        league = self.collection.find_one({"_id": self._id})

        if not league:
            # Can't find that ID
            raise AttributeError()

        self.name = league['name']  # Display Name
        self.participants = league['participants']  # List of User IDs
        self.creator = league['creator']  # The Creator of the League
        self.leagues = league['leagues']  # List of Soccer League IDs

    def add_user(self, user):
        if user._id in self.participants:
            return None

        coll = self.collection
        coll.update_one(
            {'_id': self._id},
            {'$push': {'participants': user._id}}
        )

        self.participants.append(user._id)

        user.update_user_leagues(self._id)

        return self

    @classmethod
    def new(cls, display_name: str, user, soccer_leagues: list):
        coll = cls.collection

        insert = coll.insert_one({
            "name": display_name,
            "creator": user._id,
            "participants": [user._id],
            "leagues": soccer_leagues
        })

        return UserLeague(insert.inserted_id)

    @classmethod
    def get_all(cls):
        coll = cls.collection

        leagues = [league for league in coll.find()]

        return leagues

    def __str__(self):
        return str(self.json())

    def json(self):
        return jsonify(
            doc_to_dict({
                "_id": self._id,
                "name": self.name,
                "creator": self.creator,
                "participants": self.participants,
                "leagues": self.leagues,
            })
        )
