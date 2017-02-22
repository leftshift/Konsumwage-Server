import datetime
from flask import jsonify, request

from . import api, operations
from ..db import db, models, deductions


@api.route("/get/history")
def get_history():
    values = models.Measurement.query.all()
    return jsonify(values)


@api.route("/get/current")
def get_current():
    return jsonify(deductions.stats())


@api.route("/put", methods=['PUT'])
def put_current():
    json = request.get_json()
    # This is hacky, because it can't handle timezones
    timestamp = datetime.datetime.strptime(json["timestamp"],
                                           "%Y-%m-%dT%H:%M:%S.%f")
    value = json["value"]
    operations.add_measurement(timestamp, value)
    return jsonify({"result": "success"})
