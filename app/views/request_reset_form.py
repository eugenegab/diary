from flask import Blueprint, render_template

request_reset_form_bp = Blueprint('request_reset_form', __name__)

@request_reset_form_bp.route('/request_reset_form', methods=['GET'])
def request_reset_form():
    return render_template('request_reset.html')
