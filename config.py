"""Flask configuration variables."""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    SERVER_NAME = os.environ.get("SERVER_NAME")


    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    if SQLALCHEMY_DATABASE_URI is None:
        # put in the user_record_app/app.db
        db_path = os.path.join(os.path.dirname(__file__), "app.db")
        db_uri = "sqlite:///{}".format(db_path)
        SQLALCHEMY_DATABASE_URI = db_uri

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV = os.environ.get("FLASK_ENV")

    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    # if SQLALCHEMY_DATABASE_URI is None:
    #     # put in the user_record_app/app.db
    #     db_path = os.path.join(os.path.dirname(__file__), "tests", "test.db")
    #     db_uri = "sqlite:///{}".format(db_path)
    #     SQLALCHEMY_DATABASE_URI = db_uri

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
