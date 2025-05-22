from flask import Blueprint, session, render_template, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash

from app.models import User
from app.extensions import db
from app.views.helpers import auth_required, confirm_reset_token
from app.views.api.check_data import check_password

import json


reset_password_bp = Blueprint("reset_password", __name__)


@reset_password_bp.route("/api/reset_password/<string:token>", methods=["POST"])
def reset_password(token):
    email = confirm_reset_token(token)
    if not email:
        return jsonify({'error': 'Ссылка недействительна или устарела'}),
    data = json.loads(request.data)
    confirm = data.get('confirm')
    password = data.get('password')
    if not confirm:
        return jsonify({'error': 'Повторите пароль'})
    if not password:
        return jsonify({'error': 'Вы не ввели пароль'})
    result, message = check_password(password, confirm)
    if not result:
        return jsonify({'error': message}), 400

    hashed_password = generate_password_hash(password)
    user = User.query.filter_by(email=email.lower()).first()
    user.password = hashed_password
    db.session.commit()
    session['user'] = user.to_dict()
    return jsonify({'ok': True}), 200
