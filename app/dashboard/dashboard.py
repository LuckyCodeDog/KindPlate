
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from common.login_required import admin_login_required
from common.user import current_user
dashboard = Blueprint("dashboard", __name__, template_folder="templates")



@dashboard.route("/")
def to_dashboard():
    user = current_user()
    name = "123"
    return render_template(f"dashboard_base.html", name="name")