from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(64), index=True)
    context = db.Column(db.String(64), index=True)