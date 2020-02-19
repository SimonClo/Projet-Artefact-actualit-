import os
basedir = os.path.abspath(os.path.dirname(__file__))
os.environ["DIALOGFLOW_PROJECT_ID"] = 'archiviste-mimbag'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'archiviste-mimbag.json'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False