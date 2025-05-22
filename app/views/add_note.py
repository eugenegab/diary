from flask import Blueprint, request, redirect, url_for, render_template, session

from .helpers import auth_required
from app.extensions import db
from app.models import Note, User


add_note_bp = Blueprint("add_note", __name__)


@add_note_bp.route("/add_note", methods=["GET", "POST"])
@auth_required
def add_note():
    user = session.get('user')
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        is_done = request.form.get("is_done", False)
        on_date = request.form.get("on_date")
        user = User.query.filter_by(id=user.get("user_id")).first()
        note = Note(title=title, content=content, user=user, user_id=user.id, is_done=is_done, on_date=on_date)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("index.index"))

    return render_template('edit_note.html')
