from flask import Blueprint, render_template


register_bp = Blueprint("registration", __name__)


@register_bp.route("/registration", methods=["GET", "POST"])
def registration():
    """Регистрация с логином и паролем"""
    return render_template("registration.html")
