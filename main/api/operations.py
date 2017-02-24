from flask_socketio import emit
from threading import Timer, Event

from .. import socketio
from ..db import operations, deductions

def add_measurement(timestamp, value):
    print("Adding Measurement at %s of %i" % (timestamp, value))
    if major_update_event.is_set():
        operations.add_measurement(timestamp, value)
        socketio.emit('major_update', deductions.stats())

        major_update_event.clear()
        major_update_timer = Timer(10.0, set_major_update_flag)
        major_update_timer.start()
    else:
        socketio.emit('minor_update', deductions.stats())

def set_major_update_flag():
    major_update_event.set()

major_update_timer = Timer(10.0, set_major_update_flag)
major_update_event = Event()
major_update_event.set()
