from flask import Blueprint, request, render_template, session, jsonify
from app.extensions import db
from app.models import User
from app.views.helpers import auth_required
import json


edit_profile_bp = Blueprint("edit_profile", __name__)


@edit_profile_bp.route("/api/edit_profile", methods=["POST"])
@auth_required
def edit_profile():
    user_s = session.get('user')
    data = json.loads(request.data)
    if user_s.get('login'):
        user = User.query.filter_by(login=user_s['login']).first()
    else:
        user = User.query.filter_by(email=user_s['email']).first()
    if data.get('field') == 'login':
        if User.query.filter_by(login=data['value']).first():
            return jsonify({'error': 'Логин уже занят'})
    if data.get('field') == 'email':
        if User.query.filter_by(email=data['value']).first():
            return jsonify({'error': 'Такой email уже зарегистрирован'})

    setattr(user, data['field'], data['value'])
    db.session.commit()
    session['user'] = user.to_dict()
    return jsonify({'success': True}), 200
