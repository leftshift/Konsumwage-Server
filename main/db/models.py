from time import mktime
import json
from . import db


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Measurement):
            return obj.to_json()

        return json.JSONEncoder.default(self, obj)


class Measurement(db.Model):
    timestamp = db.Column(db.DateTime, primary_key=True)
    time_delta = db.Column(db.Interval)
    consumtion = db.Column(db.Float)  # Cumulative Consumtion over time
    consumtion_delta = db.Column(db.Float)  # Delta to previous measurement

    weight = db.Column(db.Float)  # Weight at time point. Ultimately irrelevant

    def __init__(self, timestamp, time_delta, consumtion, consumtion_delta, weight):
        self.timestamp = timestamp
        self.time_delta = time_delta
        self.consumtion = consumtion
        self.consumtion_delta = consumtion_delta
        self.weight = weight

    def __repr__(self):
        return "<Measurement at %s>" % (self.timestamp)

    def to_json(self):
        return {"timestamp": mktime(self.timestamp.timetuple()),
                "time_delta": self.time_delta.total_seconds(),
                "consumtion": self.consumtion,
                "consumtion_delta": self.consumtion_delta,
                "weight": self.weight}
