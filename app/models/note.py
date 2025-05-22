from app.extensions import db
from datetime import datetime
from tzlocal import get_localzone
import pytz


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    on_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='notes')

    def to_dict(self, format_date='iso'):
        if format_date == 'iso':
            on_date = self.on_date.isoformat()
        elif format_date == 'rus':
            on_date = self.on_date.strftime('%d.%m.%Y')
        else:
            on_date = self.on_date
        tz = get_localzone()
        utc_date = pytz.utc.localize(self.created)
        return dict(
            note_id=self.id,
            title=self.title,
            content=self.content,
            is_done=self.is_done,
            created=utc_date.astimezone(tz).strftime('%d.%m.%Y %H:%M:%S'),
            updated=self.updated,
            user_id=self.user_id,
            on_date=on_date,
        )

    def __repr__(self):
        return '<Note id: {id}>'.format(id=self.id)