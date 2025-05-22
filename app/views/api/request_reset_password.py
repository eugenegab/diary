from flask import Blueprint, url_for, jsonify, request, session
from flask_mail import Message

from app.extensions import mail
from app.views.helpers import generate_token
from app.views.api.check_data import check_email
import json


request_reset_password_bp = Blueprint("request_reset_password", __name__)


@request_reset_password_bp.route("/api/request_reset_password/", methods=["POST"])
def request_reset_password():
    data = json.loads(request.data)
    email = data.get("email")
    if not email:
        if session.get("user"):
            email = session['user']['email']
        else:
            return jsonify({'error': 'Не указан email'}), 400

    result, message, status = check_email(email, exist=True)
    if not result:
        return jsonify({'error': message}), status

    token = generate_token(email)
    link = url_for('reset_password_form.reset_password_form', token=token, _external=True)

    msg = Message("Сброс пароля My Diary", recipients=[email])
    msg.body = f"Чтобы сбросить пароль, перейдите по ссылке: {link}"
    mail.send(msg)
    return jsonify({'ok': True}), 200
