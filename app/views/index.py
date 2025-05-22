from flask import Blueprint, render_template, session
from datetime import date
from app.models import Note
from .helpers import auth_required


index_bp = Blueprint("index", __name__)


@index_bp.route("/")
@index_bp.route("/<string:wanted_date>")
@auth_required
def index(wanted_date=''):
    user = session.get('user')
    if not wanted_date:
        wanted_date = date.today()
    else:
        wanted_date = date.fromisoformat(wanted_date)
    notes = [note.to_dict(format_date='rus') for note in Note.query.filter_by(user_id=user['user_id']).all()
             if note.on_date.day == wanted_date.day and note.on_date.month == wanted_date.month and note.on_date.year == wanted_date.year]
    data = {'name': user['name'] or user['login'], 'notes': notes}
    return render_template('index.html', data=data, setted_date=wanted_date.isoformat())

