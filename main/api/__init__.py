from flask import Blueprint

from .. import socketio

api = Blueprint('api', __name__)

from . import routes


@api.route("/test")
def test():
    socketio.emit('new_values', {'values': "test124"})
    return "success"
