from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from app import db
from app.models.user import User
from app.models.order import Order
from app.common.login_required import login_required
from app.common.user import current_user  



home = Blueprint("home", __name__, template_folder="templates")


@home.route("/")
def index():
    user = current_user()
    return render_template("restaurant_index.html", user=user)