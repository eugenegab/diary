from flask import Blueprint, request, render_template, Response, session

from .helpers import auth_required
from app.models import Note


note_detail_bp = Blueprint("note_detail", __name__)


@note_detail_bp.route("/notes/<int:note_id>", methods=["GET"])
@auth_required
def note_detail(note_id):
    user = session.get('user')
    if not note_id:
        return Response("Bad Request", status=400, mimetype="text/plain")
    note = Note.query.filter_by(id=note_id, user_id=user.get('user_id')).first()
    return render_template("note_detail.html", note=note)
