"""This is where the flask app's configurations are setup,
to use the correct database for when running the app."""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuration settings for running the Flask app"""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "library.db")
