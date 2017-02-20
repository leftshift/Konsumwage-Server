from flask_socketio import emit

from .. import socketio
from ..db import operations, deductions


def add_measurement(timestamp, value):
    print("Adding Measurement at %s of %i" % (timestamp, value))
    operations.add_measurement(timestamp, value)
    socketio.emit('new_values', deductions.stats())
