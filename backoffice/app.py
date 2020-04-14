from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(
    __name__,
    static_url_path='',
    static_folder='web/static',
    template_folder='web/templates')
app.config.from_object(Config)
db = SQLAlchemy(app)
import routes, models

if __name__ == "__main__":
    app.run()