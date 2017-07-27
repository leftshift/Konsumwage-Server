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
    timestamp = datetime.datetime.fromtimestamp(json["timestamp"])
    value = json["value"]
    operations.add_measurement(timestamp, value)
    return jsonify({"result": "success"})
