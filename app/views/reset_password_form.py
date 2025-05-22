from flask import render_template, Blueprint


reset_password_form_bp = Blueprint("reset_password_form", __name__)


@reset_password_form_bp.route("/reset_password_form/<string:token>", methods=["GET"])
def reset_password_form(token):
    return render_template('reset_password.html', token=token)
