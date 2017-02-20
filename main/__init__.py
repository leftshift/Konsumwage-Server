import eventlet
eventlet.monkey_patch()  # magic to make socketio work from threads
# https://github.com/miguelgrinberg/python-socketio/issues/16#issuecomment-195152403

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from .db import db
from .db.models import CustomEncoder

socketio = SocketIO(logger=True)


def create_app(debug=False, testing=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = ''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

    app.json_encoder = CustomEncoder

    from .frontend import frontend
    app.register_blueprint(frontend)

    from .api import api
    app.register_blueprint(api, url_prefix="/api")

    socketio.init_app(app)
    db.init_app(app)

    if testing:
        from .test import randomize_weight
        randomize_weight.start_generating(app.app_context())
    return app
