from flask import Blueprint, request, render_template, session, jsonify, redirect, url_for
from werkzeug.security import check_password_hash
import json

from app.models import User


login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["POST"])
def log_in():
    """Авторизация с логином и паролем"""
    try:
        data = json.loads(request.data)
        login = data.get("login")
        password = data.get("password")
        user = User.query.filter_by(login=login).first()
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
        if not check_password_hash(user.password, password):
            return jsonify({'error': 'Неверный пароль'}), 401

        session['user'] = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'login': user.login,
        }
        return jsonify('successful'), 200

    except Exception as ex:
        return render_template("login.html", error=str(ex))
