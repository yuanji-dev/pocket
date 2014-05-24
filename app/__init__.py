#encoding=utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
#use encoding=utf-8
login_manager.login_message = u'你好'
bs = Bootstrap()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    bs.init_app(app)
    #avoid circular import.
    from app.views import main

    app.register_blueprint(main)

    return app

