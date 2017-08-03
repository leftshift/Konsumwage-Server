import datetime
from flask_socketio import emit
from threading import Timer, Event

from .. import socketio
from ..db import db, models, operations, deductions


def minor_update(value):
    return operations.calulate_minor_update(value)


def add_measurement(timestamp, value):
    print("Revieved Measurement at %s of %i" % (timestamp, value))
    if major_update_event.is_set():
        operations.add_measurement(timestamp, value)
        socketio.emit('major_update', deductions.stats())

        major_update_event.clear()
        major_update_timer = Timer(5.0, set_major_update_flag)
        major_update_timer.start()
    else:
        socketio.emit('minor_update', minor_update(value))  # need to factor in factor


def set_major_update_flag():
    major_update_event.set()

major_update_timer = Timer(10.0, set_major_update_flag)
major_update_event = Event()
major_update_event.set()
