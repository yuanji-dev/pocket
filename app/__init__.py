from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)

    #avoid circular import.
    from app.views import main

    app.register_blueprint(main)

    return app

