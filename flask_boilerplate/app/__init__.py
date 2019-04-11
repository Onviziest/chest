from flask import Flask

from app.routes import register_routes
from app.models import Model


def configure_db_session(app):
    app.before_request(Model.register_session)
    app.after_request(Model.remove_session)


def migrate_database(app):
    Model.setup()


def configured_app():
    app = Flask(__name__)
    register_routes(app)
    migrate_database(app)
    configure_db_session(app)
    return app
