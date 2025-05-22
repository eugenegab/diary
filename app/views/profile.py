from flask import Blueprint, render_template, request, session

from .helpers import auth_required

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@auth_required
def profile():
    user = session.get("user")
    return render_template('profile.html', user=user, back_url=request.referrer)
