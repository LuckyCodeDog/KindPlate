import datetime
import os
from flask import Response, redirect, request, send_file
from flask import url_for
from flask import flash
import csv
from flask import current_app as app
from flask_login import login_user, logout_user
from sqlalchemy import String, cast
from app.common.MyEnum import Role
from app.models.user import User
from sqlalchemy.orm import joinedload
from app.models.order import Order
from app.models.restaurant_profile import RestaurantProfile
from app.models.menu_item import MenuItem
from app.common.forms import LoginForm, MenuItemForm, RegisterForm, UserEditForm, UserForm, changePasswordForm, RestaurantProfileForm
from flask_wtf import FlaskForm
from flask import Blueprint, redirect, render_template, url_for
from app.common.salt import password_salt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import aliased
from app.common.login_required import dashboard_roles_required
dashboard = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard.route("/")
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def main():
    return redirect(url_for("dashboard.overview"))


@dashboard.route("/overview")
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def overview():

    return render_template(f"dashboard_overview.html", name="name")


@dashboard.route("/menu_items", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def menu_item_list():
    if request.method == "GET":
        search = request.args.get('search', None)  
        page = request.args.get('page', 1, type=int)  
        per_page = 10  
        if search:
            items = MenuItem.query.filter(
                (MenuItem.name.ilike(f"%{search}%"))
            ).paginate(page=page, per_page=per_page)
        else:
            items = MenuItem.query.paginate(page=page, per_page=per_page)

        return render_template("dashboard_menu_items.html", items=items, search=search)


@dashboard.route("/menu_items/add", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def add_menu_item():
    if request.method == "POST":
        form = MenuItemForm()
        if form.validate_on_submit():
            MenuItem.create_menu_item(name=form.name.data, description=form.description.data, price=form.price.data, category=form.category.data, available=form.available.data, image_url=form.image_url.data)
            flash("Menu item added successfully", "success")
        return redirect(url_for("dashboard.menu_items_list"))
    return render_template("dashboard_menu_item_add.html")


@dashboard.route("/menu_items/edit/<int:menu_item_id>", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def edit_menu_item(menu_item_id):
    menu_item = MenuItem.get_by_id(menu_item_id)
    if not menu_item:
        flash("Menu item not found", "danger")
        return redirect(url_for("dashboard.menu_items_list"))
    
    menu_item_form = MenuItemForm( 
                                  name = menu_item.name, 
                                  description = menu_item.description, 
                                  price = menu_item.price, 
                                  category = menu_item.category, 
                                  available = menu_item.available
                                  )
    
    if request.method == "POST":
        form = MenuItemForm()
        if form.validate_on_submit():
            file = form.image.data
            filpath = app.config['UPLOAD_FOLDER'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 
            MenuItem.update(menu_item_id, name=form.name.data, description=form.description.data, price=form.price.data, category=form.category.data,image_url= image_url, available=form.available.data)
            flash("Menu item updated successfully", "success")
        return redirect(url_for("dashboard.menu_item_list"))
    return render_template("dashboard_menu_item_edit.html", form=menu_item_form, image_url=menu_item.image_url, pagetitle="Edit "+ menu_item.name)


#create a new menu item
@dashboard.route("/menu_items/create", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def create_menu_item():
    if request.method == "POST":
        form = MenuItemForm()
        if form.validate_on_submit():
            file = form.image.data
            filpath = app.config['UPLOAD_FOLDER'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 
            MenuItem.create_menu_item(name=form.name.data, description=form.description.data, price=form.price.data, category=form.category.data, image_url=image_url, available=form.available.data)
            flash("Menu item added successfully", "success")
        return redirect(url_for("dashboard.menu_item_list"))
    pagetitle = "Create Menu Item"
    return render_template("dashboard_menu_item_add.html" , pagetitle=pagetitle, form=MenuItemForm())


@dashboard.route("/menu_items/delete/<int:menu_item_id>", methods=["GET"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def delete_menu_item(menu_item_id):
    menu_item = MenuItem.get_by_id(menu_item_id)
    if not menu_item:
        flash("Menu item not found", "danger")
        return redirect(url_for("dashboard.menu_items_list"))
    MenuItem.delete(menu_item_id)
    flash("Menu item deleted successfully", "success")
    return redirect(url_for("dashboard.menu_item_list"))


@dashboard.route("/export_menu_items_csv")
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def export_menu_items_csv():
    try:
        output = export_menu_items()
        
        directory = os.path.join(os.getcwd(), "exports")
        
        if not os.path.exists(directory):
            os.makedirs(directory)  
        
        file_path = os.path.join(directory, "menu_items.csv")
        

        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=output[0].keys())
            writer.writeheader()
            for row in output:
                writer.writerow(row)
                
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return Response(str(e), status=500)

def export_menu_items():
    menu_items = MenuItem.query.all()
    output = []
    for menu_item in menu_items:
        output.append({
            "Name": menu_item.name,
            "Description": menu_item.description,
            "Price": menu_item.price,
            "Category": menu_item.category,
            "Available": menu_item.available,
        })
    return output
# water saving 

# === Menu Item End ===


@dashboard.route("/users")
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def users_list():
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    query = User.query
    query = query.filter(User.is_deleted == False)  # Filter out deleted users
    if search:
        query = query.filter(
            (User.first_name.ilike(f"%{search}%")) | (User.last_name.ilike(f"%{search}%"))
        )
    
    # Paginate the query
    users = query.paginate(page=page, per_page=per_page)
    
    # Render the template with the users and search term
    return render_template("dashboard_users.html", items=users, search=search)


@dashboard.route("/users/add", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def add_user():
    form = UserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            #check if the user already exists
            user = User.get_user_by_username(form.username.data)
            if user:
                flash("User already exists", "danger")
                return render_template("dashboard_users_add.html", form=form, pagetitle="Add User")
            file  = form.image.data
            filpath = app.config['UPLOAD_FOLDER'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 
            password_hash = generate_password_hash(form.password.data + password_salt())
           
            User.create_user(
                             username=form.username.data,
                             password_hash=password_hash,
                             email=form.email.data, 
                             phone_number=form.phone_number.data, 
                             role=form.role.data, 
                             first_name=form.first_name.data, 
                             last_name=form.last_name.data, 
                             contribution=form.contribution.data, 
                             image_url = image_url
                             )
            flash("User added successfully", "success")
        return redirect(url_for("dashboard.users_list"))
    return render_template("dashboard_users_add.html" , form=form , pagetitle="Add User")


#delete user
@dashboard.route("/users/delete/<int:user_id>", methods=["GET"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def delete_user(user_id):
    user = User.get_user_by_id(user_id)
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("dashboard.users_list"))
    User.update_user(user_id, is_deleted=True)
    flash("User deleted successfully", "success")
    return redirect(url_for("dashboard.users_list"))

#export users to csv
@dashboard.route("/export_users_csv")
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def export_users_csv():
    try:
        output = export_users()
        
        directory = os.path.join(os.getcwd(), "exports")
        
        if not os.path.exists(directory):
            os.makedirs(directory)  
        
        file_path = os.path.join(directory, "users.csv")
        

        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=output[0].keys())
            writer.writeheader()
            for row in output:
                writer.writerow(row)
                
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return Response(str(e), status=500)


def export_users():
    users = User.query.all()
    output = []
    for user in users:
        output.append({
            "Username": user.username,
            "Email": user.email,
            "Phone Number": user.phone_number,
            "Role": user.role,
            "First Name": user.first_name,
            "Last Name": user.last_name,
            "Contribution": user.contribution,
            "Status": user.status,
        })
    return output
#edit user  


@dashboard.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def edit_user(user_id):
    user = User.get_user_by_id(user_id)
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("dashboard.users_list"))
    form = UserEditForm(
                    email=user.email,
                    phone_number=user.phone_number,
                    role=user.role,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    contribution=user.contribution,
                    status=user.status
                    )
    if request.method == "POST":
        if form.validate_on_submit():
            file = form.image.data
            filpath = app.config['UPLOAD_FOLDER'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 
            User.update_user(
                            user_id=user_id,
                            
                            email=form.email.data, 
                             
                             phone_number=form.phone_number.data, 
                             
                             role=form.role.data, 
                             
                             first_name=form.first_name.data, 
                             
                             last_name=form.last_name.data, 
                             
                             contribution=form.contribution.data, 
                             
                             image_url = image_url, 
                             
                             status=form.status.data
                             
                             )
            flash("User updated successfully", "success")
            return redirect(url_for("dashboard.users_list"))
    return render_template("dashboard_users_edit.html", form=form, pagetitle="Edit User")

#reset password
@dashboard.route("/users/reset_password/<int:user_id>", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def reset_password(user_id):
    
    user = User.get_user_by_id(user_id)
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("dashboard.users_list"))
    form = changePasswordForm()
    if request.method == "GET":
        return render_template("dashboard_users_reset_password.html", form=form)
    if form.validate():
        # updated the password  
        User.update_user(user_id, password_hash=generate_password_hash(form.new_password.data + password_salt()))
        flash("Password reset successfully", "success")
        return redirect(url_for("dashboard.users_list"))
    return render_template("dashboard_users_reset_password.html", form=form, pagetitle="Reset Password")

# === User Management End ===

# === settings ===
@dashboard.route("/settings", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def settings():
    if request.method == "POST":
        # Handle form submission for settings here
        form = RestaurantProfileForm()
        if form.validate_on_submit():
            # Update the restaurant profile with the form data
            file = form.image.data
            filpath = app.config['UPLOAD_FOLDER'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 

            RestaurantProfile.update_profile(
                profile_id=1,  # Assuming you have only one profile
                description=form.description.data,
                rating=form.rating.data,
                facilities=form.facilities.data,
                opening_date=form.opening_date.data,
                opening_time=form.opening_time.data,
                closing_time=form.closing_time.data,
                image_url=image_url
            )
            flash("Settings updated successfully", "success")
        return redirect(url_for("dashboard.settings"))
    
    # Render the settings page

    restaurant  =   RestaurantProfile.get_profile_by_id(1)

    form = RestaurantProfileForm(
        description=restaurant.description,
        rating=restaurant.rating,
        facilities=restaurant.facilities,
        opening_date=restaurant.opening_date,
        opening_time=restaurant.opening_time,
        closing_time=restaurant.closing_time,
        image_url=restaurant.image_url
    )

    return render_template("dashboard_settings.html", form=form, restaurant=restaurant)

# === settings ===

# === Order Management ===
# == Order List ==
@dashboard.route("/orders")
@dashboard_roles_required(Role.Admin.value, Role.Waiter.value, Role.Chef.value)
def orders_list():
    Customer = aliased(User)
    Waiter = aliased(User)

    if request.method == "GET":
        search = request.args.get('search', None)  
        page = request.args.get('page', 1, type=int)  
        per_page = 5 
        orders = None
        if search:
            orders = Order.query.join(Customer, Order.customer_id == Customer.user_id).join(Waiter, Order.waiter_id == Waiter.user_id).filter(
            cast(Order.order_id, String).ilike(f"%{search}%")).paginate(page=page, per_page=per_page)
            print(orders)
        else:
            orders = Order.query \
                .options(joinedload(Order.customer), joinedload(Order.waiter)) \
                .paginate(page=page, per_page=per_page)
        return render_template("dashboard_orders.html", items=orders, search=search)

@dashboard.route("/docs")
def docs():
    return render_template("docs.html")

@dashboard.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if request.method == "POST":
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username_or_email.data).first()

            if user and user.username =="admin1":
                login_user(user)
                flash(f"Login successful, welcome !", "success")
                return redirect(url_for("dashboard.main"))
            if user and check_password_hash(user.password_hash, login_form.password.data):
                login_user(user)
                flash(f"Login successful, welcome !", "success")
                return redirect(url_for("dashboard.main"))
            else:
                flash("Invalid credentials", "danger")  
        flash("Invalid credentials", "danger")  
        return redirect(url_for("dashboard.login"))      
    return render_template("dashboard_login.html", login_form=login_form)

# logout
@dashboard.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("dashboard.login"))