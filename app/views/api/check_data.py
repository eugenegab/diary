from flask import Blueprint, jsonify, request
import json
from app.models import User
from email_validator import validate_email, EmailNotValidError


check_data_bp = Blueprint("check_data", __name__)
ALLOWED_CHARACTERS = '-_.,@!$%#'
UPPER_LETTERS = list(range(ord('A'), ord('Z')+1))
LOWER_LETTERS = list(range(ord('a'), ord('z')+1))
UPPER_CYRILLIC = list(range(ord('А'), ord('Я')+1))
LOWER_CYRILLIC = list(range(ord('а'), ord('я')+1))
DIGITS = list(range(ord('0'), ord('9')))
PASSWORD_CHARACTERS_CODES = [ord(char) for char in ALLOWED_CHARACTERS] + LOWER_LETTERS + UPPER_LETTERS + DIGITS + LOWER_CYRILLIC + UPPER_CYRILLIC
LOGIN_CHARACTERS_CODES = UPPER_LETTERS + LOWER_LETTERS + DIGITS + ['_']


@check_data_bp.route("/api/check_data", methods=["POST"])
def check_data():
    data = json.loads(request.data)
    if not data.get("email"):
        return jsonify({"error": "Вы не указали email"}), 400
    elif not data.get("password"):
        return jsonify({"error": "Вы не указали пароль"}), 400
    elif not data.get("login"):
        return jsonify({"error": "Вы не указали логин"}), 400
    elif not data.get("confirm"):
        return jsonify({'error': "Повторите пароль"}), 400

    password = data.get("password")
    email = data.get("email")
    login = data.get("login")
    confirm = data.get("confirm")

    result, message = check_password(password, confirm)
    if not result:
        return jsonify({"error": message}), 400

    result, message, status = check_email(email)
    if not result:
        return jsonify({"error": message}), status

    for char in login:
        if ord(char) not in LOGIN_CHARACTERS_CODES:
            return jsonify({'error': 'В логине не допустимые символы. Можно использовать только прописные и заглавные латинские буквы, "_" и цифры'}), 400

    user_with_login = User.query.filter_by(login=login).first()
    user_with_email = User.query.filter_by(email=email.lower()).first()
    if user_with_login:
        return jsonify({'error': 'Пользователь с таким логином уже зарегистрирован'}), 400
    if user_with_email:
        return jsonify({'error': 'Пользователь с таким email уже зарегистрирован'}), 400
    return jsonify({"ok": True}), 200


def check_password(password, confirm):
    is_there_lower = False
    is_there_upper = False
    is_there_digit = False
    if len(password) < 8:
        return False, 'Пароль слишком короткий'
    for char in password:
        if ord(char) not in PASSWORD_CHARACTERS_CODES:
            return False, 'В пароле недопустимые символы'
        if ord(char) in LOWER_LETTERS + LOWER_CYRILLIC:
            is_there_lower = True
        if ord(char) in UPPER_LETTERS + UPPER_CYRILLIC:
            is_there_upper = True
        if ord(char) in DIGITS:
            is_there_digit = True
    if not (is_there_lower and is_there_upper and is_there_digit):
        return False, 'Некорректный пароль'
    if password != confirm:
        return False, 'Пароли не совпадают'
    return True, ''


def check_email(email, exist=False):
    try:
        validate_email(email, check_deliverability=True)
    except EmailNotValidError as e:
        return False, 'Некорректный email', 400
    user = User.query.filter_by(email=email.lower()).first()
    if user and not exist:
        return False, 'Пользователь с таким email уже существует', 400
    elif not user and exist:
        return False, 'Пользователя с таким email нет', 404
    return True, '', 200
