
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
dashboard = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard.route("/")
def to_dashboard():
    user = current_user()
    name = "123"
    user = User.get_all_users()
    order = Order.get_all_orders()
    print(order)
   # User.create_user(username="admin", password_hash="admin", email="123@123.com", phone_number="12345678901", role="Admin")
    print(user)
    return render_template(f"dashboard_overview.html", name="name")

