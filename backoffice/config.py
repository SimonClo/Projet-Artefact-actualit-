import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@database:5432/artefact_archives"
    SQLALCHEMY_TRACK_MODIFICATIONS = False