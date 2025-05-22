from flask import Blueprint, request, redirect, url_for, render_template, Response, session
from app.extensions import db
from .helpers import auth_required
from app.models import Note


edit_note_bp = Blueprint("edit_note", __name__)


@edit_note_bp.route("/edit_note/<int:note_id>", methods=["GET", "POST"])
@auth_required
def edit_note(note_id):
    user = session.get('user')
    if not note_id:
        return Response('Bad Request', 400, mimetype="text/plain")

    note = Note.query.filter_by(id=note_id, user_id=user.get('user_id')).first()

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        is_done = request.form.get("is_done", False)
        note.title = title
        note.content = content
        note.is_done = True if is_done else False
        db.session.commit()
        return redirect(url_for("note_detail.note_detail", note_id=note.id))

    return render_template('edit_note.html', note=note.to_dict(), back_url=request.referrer)
