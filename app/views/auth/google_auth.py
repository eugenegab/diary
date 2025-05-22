from flask import Blueprint, redirect, url_for, session

from app.extensions import db
from app.google_client import google_oauth  # <-- просто импортируешь
from app.models import User
import secrets


auth_bp = Blueprint("google_auth", __name__)
token_urlsafe_size = 32


@auth_bp.route('/auth/google')
def login():
    """Авторизация с Google"""
    nonce = secrets.token_urlsafe(token_urlsafe_size)
    session['nonce'] = nonce
    redirect_uri = url_for('google_auth.auth_callback', _external=True)
    return google_oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

@auth_bp.route('/auth/google/callback')
def auth_callback():
    token = google_oauth.google.authorize_access_token()
    nonce = session['nonce']

    user_info = google_oauth.google.parse_id_token(token, nonce=nonce)
    user = User.query.filter_by(email=user_info['email'].lower()).first()

    if not user:
        user = User(login=user_info['email'],
                    email=user_info['email'],
                    name=user_info.get('given_name'))
        db.session.add(user)
        db.session.commit()
    if not user.name:
        user.name = user_info['given_name']
        db.session.commit()

    session['user'] = {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'login': user.login,
    }

    return redirect(url_for('index.index'))