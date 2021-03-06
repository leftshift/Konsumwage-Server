from time import mktime
import json
from . import db


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Measurement):
            return obj.to_json()

        return json.JSONEncoder.default(self, obj)


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    consumption_delta = db.Column(db.Float)  # Delta to previous measurement

    weight = db.Column(db.Float)  # Weight at time point. Ultimately irrelevant

    def __init__(self, timestamp, consumption_delta, weight):
        self.timestamp = timestamp
        self.consumption_delta = consumption_delta
        self.weight = weight

    def __repr__(self):
        return "<Measurement at %s>" % (self.timestamp)

    def to_json(self):
        return {"timestamp": mktime(self.timestamp.timetuple()),
                "consumption_delta": self.consumption_delta,
                "weight": self.weight}
