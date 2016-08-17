from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Entry(db.Model):
    # Constants
    TYPE_TEXT = 1
    TYPE_IMG = 2

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    content_type = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)

    def __init__(self, content, content_type):
        self.content = content
        self.content_type = content_type
        self.datetime = datetime.utcnow()

    def __str__(self):
        return '<Entry #{}>'.format(self.id)

    @staticmethod
    def get_text_entries(count=10):
        return Entry.query.filter_by(content_type=Entry.TYPE_TEXT).order_by('datetime desc').limit(count)
