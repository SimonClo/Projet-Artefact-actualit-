from app import db

class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    _prev_action = db.Column(db.String(64), index=True)
    _context = db.Column(db.String(64), index=True)
    _last_article_seen = db.Column(db.Integer, index=True)
    _rank_last_archive = db.Column(db.Integer, index=True)

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

    @property
    def last_article_seen(self):
        return self._last_article_seen

    @last_article_seen.setter
    def last_article_seen(self, value):
        self._last_article_seen = value

    @property
    def rank_last_archive(self):
        return self._rank_last_archive

    @rank_last_archive.setter
    def rank_last_archive(self, value):
        self._rank_last_archive = value