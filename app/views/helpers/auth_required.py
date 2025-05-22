from flask import session, render_template, request
from app.models import User
import functools


def auth_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        user = session.get('user')
        if not user:
            return render_template("login.html")
        login, email = user.get('login'), user.get('email')
        if login:
            user = User.query.filter_by(login=login).first()
        elif email:
            user = User.query.filter_by(email=email).first()
        if not user:
            session.pop('user')
            return render_template("login.html")
        session['user'] = user.to_dict()
        return view(*args, **kwargs)
    return wrapped_view
