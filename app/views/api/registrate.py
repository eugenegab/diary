from flask import Blueprint, session, redirect, url_for, Response, request
from app.extensions import db

from app.models import User
from app.views.helpers import confirm_reset_token
from werkzeug.security import generate_password_hash


registrate_bp = Blueprint('registrate', __name__)


@registrate_bp.route('/api/registrate', methods=['GET'])
def registrate():
    registration_data = session['registration_data']
    token = request.args.get('token')
    login = registration_data.get('login')
    password = registration_data.get('password')
    name = registration_data.get('name', '')
    email = confirm_reset_token(token)
    if not email:
        return Response('Ссылка недействительна или устарела', status=401)
    try:
        hashed_password = generate_password_hash(password)
        user = User(login=login, password=hashed_password, name=name, email=email.lower())
        db.session.add(user)
        db.session.commit()

        session['user'] = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'login': user.login,
        }
        return redirect(url_for('index.index'))
    except Exception as e:
        return Response('Произошла ошибка, попробуйте еще раз', status=500)
