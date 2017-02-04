from flask import Blueprint

from .. import socketio

websocket_api = Blueprint('websocket_api', __name__)


@websocket_api.route("/test")
def test():
    socketio.emit('new_values', {'values': "test124"})
    return "success"
