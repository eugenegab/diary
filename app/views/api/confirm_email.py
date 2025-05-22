from flask import Blueprint, url_for, jsonify, request, session
from app.extensions import mail
from flask_mail import Message
import json

from app.views.helpers import generate_token


confirm_email_bp = Blueprint('confirm_email', __name__)


@confirm_email_bp.route('/confirm_email', methods=['POST'])
def confirm_email():
    data = json.loads(request.data)
    email = data.get('email')
    login = data.get('login')
    password = data.get('password')
    name = data.get('name', '')
    if not email or not login or not password:
        return jsonify({'error': 'Некорректный запрос'}), 400

    token = generate_token(email)
    session['registration_data'] = {'login': login, 'password': password, 'name': name}
    link = url_for('registrate.registrate', token=token, _external=True)

    msg = Message("Подтверждение email на My Diary", recipients=[email])
    msg.body = f"Чтобы подтвердить email, перейдите по ссылке: {link}"
    mail.send(msg)
    return jsonify({'ok': True}), 200
