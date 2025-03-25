
import datetime
from flask import Blueprint, send_file, Response
from flask import render_template
from flask import request
import os
from flask import redirect
from flask import url_for
from flask import flash
import csv
from flask import current_app as app
from app.models.user import User
from app.models.order import Order
from app.models.menu_item import MenuItem
from app.common.login_required import login_required
from app.common.user import current_user
from app.common.forms import MenuItemForm, UserForm
from flask_wtf import FlaskForm
from app.dashboard import dashboard
# === Menu Item  ===

@dashboard.route("/")
def main():
    return redirect(url_for("dashboard.overview"))

@dashboard.route("/overview")
def overview():

    return render_template(f"dashboard_overview.html", name="name")


# === User Management ===
@dashboard.route("/users")
def users_list():
    # pagnation
    page = request.args.get('page', 1, type=int)
    per_page = 10
    users = User.query.paginate(page=page, per_page=per_page)
    return render_template("dashboard_users.html", items=users)
@dashboard.route("/users/add", methods=["GET", "POST"])
def add_user():
    form = UserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            User.create_user(username=form.username.data, password_hash=form.password_hash.data, email=form.email.data, phone_number=form.phone_number.data, role=form.role.data, first_name=form.first_name.data, last_name=form.last_name.data, contribution=form.contribution.data, image_url=form.image_url.data, status=form.status.data)
            flash("User added successfully", "success")
        return redirect(url_for("dashboard.users_list"))
    return render_template("dashboard_users_add.html" , form=form , pagetitle="Add User")
# === User Management End ===
@dashboard.route("/docs")
def docs():
    return render_template("docs.html")