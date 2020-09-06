import datetime
import json

from bson import ObjectId

from src.util.util import DEFAULT_DATE_FORMAT


class JSONEncoder(json.JSONEncoder):
    """Simple encoder class to handle ObjectId to json conversion"""

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)

        if isinstance(obj, datetime.datetime):
            return obj.strftime(DEFAULT_DATE_FORMAT)

        return json.JSONEncoder.default(self, obj)


def doc_to_dict(obj: any):
    """Convert a Mongo document to a json friendly dictionary.

    Wrapper for JSONEncoder().encode(obj)
    """

    as_str = JSONEncoder().encode(obj)
    as_dict = json.loads(as_str)

    return as_dict
