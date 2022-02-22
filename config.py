import os


class BaseConfig:
    # app
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    BASE_DIR = os.path.join(APP_DIR, 'app/db_app.db')
    SECRET_KEY = 'my_secret_key'
    DEBUG = True
    # db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QSLALCHEMY_COMMIT_ON_TEARDOWN = True