from flask import Blueprint, request, redirect, url_for, jsonify, session

from .helpers import auth_required
from app.extensions import db
from app.models import Note


delete_note_bp = Blueprint("delete_note", __name__)


@delete_note_bp.route("/delete_note/<int:note_id>", methods=["POST"])
@auth_required
def delete_note(note_id):
    user = session.get('user')
    try:
        if request.method == "POST":
            note = Note.query.filter_by(id=note_id, user_id=user.get('user_id')).first()
            db.session.delete(note)
            db.session.commit()
            return redirect(url_for("index.index"))

    except Exception as e:
        return jsonify({'error': str(e)}), 500
