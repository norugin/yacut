from datetime import datetime, UTC
from random import choice
import string

from flask import url_for

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(512), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(UTC))

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('short_link_url',
                               short_id=self.short,
                               _external=True)
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])

    def is_short_link_exists(self, custom_id):
        return bool(self.query.filter_by(short=custom_id).first())

    def get_unique_short_id(self):
        short_id = ""
        symbols = string.ascii_letters + string.digits
        while len(short_id) != 6:
            short_id += choice(symbols)

        if self.is_short_link_exists(short_id):
            return self.get_unique_short_id()
        return short_id

    def is_valid_short_id(self, short_id):
        symbols = string.ascii_letters + string.digits
        if len(short_id) > 16:
            return False
        for value in short_id:
            if value not in symbols:
                return False
        return True
