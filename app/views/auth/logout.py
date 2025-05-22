from flask import Blueprint, render_template, session, redirect, url_for

from app.views.helpers import auth_required


logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout")
@auth_required
def logout():
    """Выход"""
    try:
        user = session.get('user')
        if user:
            session.pop("user")
        return redirect(url_for('index.index'))

    except Exception as ex:
        return render_template("login.html", error=str(ex))
