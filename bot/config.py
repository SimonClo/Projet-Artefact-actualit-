import os

basedir = os.path.abspath(os.path.dirname(__file__))
os.environ["DIALOGFLOW_PROJECT_ID"] = 'archiviste-mimbag'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'archiviste-mimbag.json'

# database credentials

DB_HOST = "database"
DB_PORT = 5432
DB_NAME = "artefact_archives"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

NUM_ARTICLES = 3
NUM_ARCHIVES = 5

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False