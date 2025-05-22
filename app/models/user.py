from app.extensions import db
from datetime import datetime
from tzlocal import get_localzone
import pytz


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    name = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        tz = get_localzone()
        utc_date = pytz.utc.localize(self.created)
        return dict(
            user_id=self.id,
            login=self.login or '',
            email=self.email or '',
            name=self.name or '',
            created=utc_date.astimezone(tz).strftime('%d.%m.%Y %H:%M:%S'),
            is_admin=self.is_admin,
        )

    def __str__(self):
        return self.name or self.login or self.email

    def __repr__(self):
        return '<User id: {id}>'.format(id=self.id)
