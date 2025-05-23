from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def confirm_reset_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        return s.loads(token, salt='password-reset', max_age=expiration)
    except Exception:
        return None
