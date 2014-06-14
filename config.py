import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    READABILITY_TOKEN = os.environ.get('READABILITY_TOKEN')
    READABILITY_API_URL = os.environ.get('READABILITY_API_URL')
    HTTP_HEADERS = {}


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-date.sqlite')
    SECRET_KEY = 'hello'
    BOOTSTRAP_SERVE_LOCAL = True
    SERVER_NAME = '127.0.0.1:9527'


class ProductionConfig(Config):
    pass