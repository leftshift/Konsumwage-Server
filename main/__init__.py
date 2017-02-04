from flask import Flask, render_template
from flask_socketio import SocketIO


socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    from .frontend import frontend
    app.register_blueprint(frontend)

    from .websocket_api import websocket_api
    app.register_blueprint(websocket_api, url_prefix="/api")

    socketio.init_app(app)
    return app
