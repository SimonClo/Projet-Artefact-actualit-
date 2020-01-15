from app import db

class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    _prev_action = db.Column(db.String(64), index=True)
    _context = db.Column(db.String(64), index=True)

    @property
    def prev_action(self):
        return self._prev_action

    @prev_action.setter
    def prev_action(self, value):
        self._prev_action = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value