import datetime
from datetime import datetime
import os
from flask import Response, redirect, request, send_file
from flask import url_for
from flask import flash
import csv
from flask import current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import String, cast
from app.common.MyEnum import Role
from app.models.booking import Booking
from app.models.user import User
from sqlalchemy.orm import joinedload
from app.models.order import Order, OrderItem
from app.models.restaurant_profile import RestaurantProfile
from app.models.menu_item import MenuItem
from app.models.ingredient import Ingredient
from app.models.meat import Meat
from app.models.menu_item_ingredient import MenuItemIngredient
from app.common.forms import LoginForm, MenuItemForm, RegisterForm, UserEditForm, UserForm, changePasswordForm, RestaurantProfileForm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DecimalField, BooleanField, FloatField
from wtforms.validators import DataRequired, Optional, NumberRange
from flask import Blueprint, redirect, render_template, url_for
from app.common.salt import password_salt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import aliased
from app.common.login_required import dashboard_roles_required
from app.models.water_saving_badge import WaterSavingBadge
from app.models.user_badge import UserBadge
from app.models.user_water_saving_history import UserWaterSavingHistory
from app.forms.badge_form import BadgeForm
from werkzeug.utils import secure_filename
from app import db
from app.forms.dashboard_forms import ManagerRegistrationForm
from urllib.parse import urlparse

dashboard = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard.route("/")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)        
def main():
    return redirect(url_for("dashboard.menu_item_list"))


@dashboard.route("/overview")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
def overview():

    return render_template(f"dashboard_overview.html", name="name")


@dashboard.route("/menu_items", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
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
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
def add_menu_item():
    if request.method == "POST":
        form = MenuItemForm()
        if form.validate_on_submit():
            MenuItem.create_menu_item(name=form.name.data, description=form.description.data, price=form.price.data, category=form.category.data, available=form.available.data, image_url=form.image_url.data)
            flash("Menu item added successfully", "success")
        return redirect(url_for("dashboard.menu_items_list"))
    return render_template("dashboard_menu_item_add.html")


@dashboard.route("/menu_items/edit/<int:menu_item_id>", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
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
            filpath = current_app.config['UPLOAD_FOLDER'] + datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 
            MenuItem.update(menu_item_id, name=form.name.data, description=form.description.data, price=form.price.data, category=form.category.data,image_url= image_url, available=form.available.data)
            flash("Menu item updated successfully", "success")
        return redirect(url_for("dashboard.menu_item_list"))
    return render_template(
        "dashboard_menu_item_edit.html", 
        form=menu_item_form, 
        image_url=menu_item.image_url, 
        menu_item_id=menu_item_id,
        pagetitle="Edit "+ menu_item.name
    )


#create a new menu item
@dashboard.route("/menu_items/create", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def create_menu_item():
    if request.method == "POST":
        form = MenuItemForm()
        if form.validate_on_submit():
            file = form.image.data
            filpath = current_app.config['UPLOAD_FOLDER'] + datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 
            MenuItem.create_menu_item(name=form.name.data, description=form.description.data, price=form.price.data, category=form.category.data, image_url=image_url, available=form.available.data)
            flash("Menu item added successfully", "success")
        return redirect(url_for("dashboard.menu_item_list"))
    pagetitle = "Create Menu Item"
    return render_template("dashboard_menu_item_add.html" , pagetitle=pagetitle, form=MenuItemForm())


@dashboard.route("/menu_items/delete/<int:menu_item_id>", methods=["GET"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def delete_menu_item(menu_item_id):
    menu_item = MenuItem.get_by_id(menu_item_id)
    if not menu_item:
        flash("Menu item not found", "danger")
        return redirect(url_for("dashboard.menu_items_list"))
    MenuItem.delete(menu_item_id)
    flash("Menu item deleted successfully", "success")
    return redirect(url_for("dashboard.menu_item_list"))


@dashboard.route("/export_menu_items_csv")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
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
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
def users_list():
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Increase to 12 users per page
    
    query = User.query
    query = query.filter(User.is_deleted == False)  # Filter out deleted users
    if search:
        query = query.filter(
            (User.first_name.ilike(f"%{search}%")) | 
            (User.last_name.ilike(f"%{search}%")) |
            (User.username.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    
    # Paginate the query
    users = query.paginate(page=page, per_page=per_page)
    
    # Render the template with the users and search term
    return render_template("dashboard_users.html", items=users, search=search)


@dashboard.route("/users/add", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
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
            filpath = current_app.config['UPLOAD_FOLDER'] + datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 
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
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
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
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
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
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
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
            filpath = current_app.config['UPLOAD_FOLDER'] + datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 
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
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
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
@dashboard_roles_required(Role.Admin.value)
def settings():
    if request.method == "POST":
        # Handle form submission for settings here
        form = RestaurantProfileForm()
        if form.validate_on_submit():
            # Update the restaurant profile with the form data
            file = form.image.data
            filpath = current_app.config['UPLOAD_FOLDER'] + datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 

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
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
def orders_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get filter parameters
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Base query
    query = Order.query
    
    # Apply filters
    if status:
        query = query.filter(Order.status == status)
    if date_from:
        query = query.filter(Order.order_date >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(Order.order_date <= datetime.strptime(date_to, '%Y-%m-%d'))
    
    # Get orders with related data
    orders = query.order_by(Order.order_date.desc()) \
        .options(joinedload(Order.customer)) \
        .paginate(page=page, per_page=per_page)
    
    return render_template('dashboard_orders.html',
                         orders=orders,
                         status=status,
                         date_from=date_from,
                         date_to=date_to)

@dashboard.route("/export_orders_csv")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
def export_orders_csv():
    try:
        output = export_orders()
        
        directory = os.path.join(os.getcwd(), "exports")
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        file_path = os.path.join(directory, "orders.csv")
        
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=output[0].keys())
            writer.writeheader()
            for row in output:
                writer.writerow(row)
                
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return Response(str(e), status=500)

def export_orders():
    orders = Order.query.all()
    output = []
    for order in orders:
        customer_name = f"{order.customer.first_name} {order.customer.last_name}" if order.customer else f"{order.first_name} {order.last_name}"
        output.append({
            "Order ID": order.order_id,
            "Customer": customer_name,
            "Order Date": order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            "Status": order.status,
            "Total Amount": f"${order.total_amount:.2f}",
            "Email": order.customer.email if order.customer else order.email,
            "Phone": order.customer.phone_number if order.customer else "N/A",
            "Address": f"{order.address}, {order.city_or_town}, {order.zip_code}" if not order.customer else "N/A"
        })
    return output

@dashboard.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('dashboard.index'))
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        try:
            # Special handling for admin1 user
            if login_form.username_or_email.data == 'admin1':
                user = User.query.filter_by(username='admin1').first()
                if user:
                    login_user(user)
                    flash('Welcome back, Admin!', 'success')
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('dashboard.main'))
                else:
                    flash('Admin account not found', 'danger')
                    return render_template('dashboard_login.html', login_form=login_form)
            
            # Normal login flow for other users
            user = User.query.filter(
                (User.username == login_form.username_or_email.data) | 
                (User.email == login_form.username_or_email.data)
            ).first()
            
            if not user:
                flash('Account not found. Please check your username/email.', 'danger')
                return render_template('dashboard_login.html', login_form=login_form)
            
            if user.is_deleted:
                flash('This account has been deactivated.', 'danger')
                return render_template('dashboard_login.html', login_form=login_form)
            
            if user.status != 'active':
                flash('Your account is not active. Please contact administrator.', 'warning')
                return render_template('dashboard_login.html', login_form=login_form)
            
            if check_password_hash(user.password_hash, login_form.password.data):
                if user.role == 'manager':
                    login_user(user, remember=login_form.remember.data)
                    flash(f'Welcome back, {user.first_name}!', 'success')
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('dashboard.main'))
                else:
                    flash('Access denied. Only managers can access the dashboard.', 'danger')
            else:
                flash('Invalid password. Please try again.', 'danger')
                
        except Exception as e:
            current_app.logger.error(f'Login error: {str(e)}')
            flash('An error occurred during login. Please try again.', 'danger')
    
    return render_template('dashboard_login.html', login_form=login_form)

@dashboard.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = ManagerRegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('dashboard.register'))
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('dashboard.register'))
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            role='manager',
            status='active'
        )
        user.set_password(form.password.data)
        
        # Handle profile image upload
        if form.image.data:
            # Create upload directory if it doesn't exist
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'users')
            os.makedirs(upload_dir, exist_ok=True)
            
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Use os.path.join for cross-platform compatibility
            file_path = os.path.join(upload_dir, filename)
            form.image.data.save(file_path)
            
            # Store the relative path in the database
            user.image_url = f"/static/uploads/users/{filename}"
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('dashboard.login'))
    
    return render_template('dashboard_register.html', form=form)

# logout
@dashboard.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("dashboard.login"))

# bookings
@dashboard.route("/bookings")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)     
def bookings_list():
    if request.method == "GET":
        search = request.args.get('search', None)  
        page = request.args.get('page', 1, type=int)  
        per_page = 5 
        bookings = None
        if search:
            bookings = Booking.query.filter(
                (Booking.first_name.ilike(f"%{search}%")) | (Booking.last_name.ilike(f"%{search}%"))
            ).paginate(page=page, per_page=per_page)
        else:
            bookings = Booking.query.paginate(page=page, per_page=per_page)
        return render_template("dashboard_bookings.html", items=bookings, search=search)
    
#change booking status
@dashboard.route("/bookings/change_status/<int:booking_id>", methods=["POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value) 
def change_booking_status(booking_id):

    #ajax
    booking = Booking.get_by_id(booking_id)
    data = request.get_json()
    new_status = data.get("status")

    if not booking:
        return {"status": "error", "message": "Booking not found"}, 404
    if new_status not in ["pending", "confirmed", "cancelled"]:
        return {"status": "error", "message": "Invalid status"}, 400
    Booking.update(booking_id, status=new_status)
    return {"status": "success", "message": "Booking status updated successfully"}, 200


# === Ingredient Management Start ===

class IngredientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    meat_id = SelectField('Meat Type', coerce=int, validators=[Optional()])
    water_usage_l_per_kg = DecimalField('Water Usage (L/kg)', validators=[DataRequired(), NumberRange(min=0)], places=2)

@dashboard.route("/ingredients")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def ingredient_list():
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Ingredient.query
    if search:
        query = query.filter(Ingredient.name.ilike(f"%{search}%"))
    
    ingredients = query.paginate(page=page, per_page=per_page)
    return render_template("dashboard_ingredients.html", items=ingredients, search=search)

@dashboard.route("/ingredients/create", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def create_ingredient():
    form = IngredientForm()
    # Get all meat options
    meats = Meat.get_all()
    form.meat_id.choices = [(0, 'None')] + [(meat.meat_id, meat.meat_type) for meat in meats]

    if request.method == "POST" and form.validate_on_submit():
        meat_id = form.meat_id.data if form.meat_id.data != 0 else None
        ingredient = Ingredient.create(
            name=form.name.data,
            description=form.description.data,
            meat_id=meat_id
        )
        if ingredient:
            flash("Ingredient added successfully", "success")
            return redirect(url_for("dashboard.ingredient_list"))
        else:
            flash("Failed to add ingredient", "danger")

    return render_template("dashboard_ingredient_add.html", form=form, pagetitle="Create Ingredient")

@dashboard.route("/ingredients/edit/<int:ingredient_id>", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def edit_ingredient(ingredient_id):
    ingredient = Ingredient.get_by_id(ingredient_id)
    if not ingredient:
        flash("Ingredient not found", "danger")
        return redirect(url_for("dashboard.ingredient_list"))

    form = IngredientForm()
    meats = Meat.get_all()
    form.meat_id.choices = [(0, 'None')] + [(meat.meat_id, meat.meat_type) for meat in meats]

    if request.method == "POST" and form.validate_on_submit():
        meat_id = form.meat_id.data if form.meat_id.data != 0 else None
        if Ingredient.update(
            ingredient_id=ingredient_id,
            name=form.name.data,
            description=form.description.data,
            meat_id=meat_id
        ):
            flash("Ingredient updated successfully", "success")
            return redirect(url_for("dashboard.ingredient_list"))
        else:
            flash("Failed to update ingredient", "danger")
    else:
        form.name.data = ingredient.name
        form.description.data = ingredient.description
        form.meat_id.data = ingredient.meat_id if ingredient.meat_id else 0

    return render_template("dashboard_ingredient_edit.html", form=form, ingredient=ingredient, pagetitle="Edit Ingredient")

@dashboard.route("/ingredients/delete/<int:ingredient_id>")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def delete_ingredient(ingredient_id):
    if Ingredient.delete(ingredient_id):
        flash("Ingredient deleted successfully", "success")
    else:
        flash("Failed to delete ingredient", "danger")
    return redirect(url_for("dashboard.ingredient_list"))

@dashboard.route("/export_ingredients_csv")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def export_ingredients_csv():
    try:
        output = export_ingredients()
        
        directory = os.path.join(os.getcwd(), "exports")
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        file_path = os.path.join(directory, "ingredients.csv")
        
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=output[0].keys())
            writer.writeheader()
            for row in output:
                writer.writerow(row)
                
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return Response(str(e), status=500)

def export_ingredients():
    ingredients = Ingredient.query.all()
    output = []
    for ingredient in ingredients:
        meat_type = ingredient.meat.meat_type if ingredient.meat else None
        output.append({
            "Name": ingredient.name,
            "Description": ingredient.description,
            "Meat Type": meat_type,
            "Created At": ingredient.created_at
        })
    return output

# === Ingredient Management End ===

class MenuItemIngredientForm(FlaskForm):
    ingredient_id = SelectField('Ingredient', coerce=int, validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=0.01)])
    unit = SelectField('Unit', choices=[('g', 'Grams'), ('kg', 'Kilograms'), ('l', 'Liters'), ('gallon', 'Gallons')], validators=[DataRequired()])

@dashboard.route("/menu_items/<int:menu_item_id>/ingredients", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def manage_menu_item_ingredients(menu_item_id):
    menu_item = MenuItem.get_by_id(menu_item_id)
    if not menu_item:
        flash("Menu item not found", "danger")
        return redirect(url_for("dashboard.menu_item_list"))

    form = MenuItemIngredientForm()
    # Get all available ingredients as options
    ingredients = Ingredient.get_all()
    form.ingredient_id.choices = [(i.ingredient_id, i.name) for i in ingredients]

    if request.method == "POST" and form.validate_on_submit():
        ingredient_id = form.ingredient_id.data
        quantity = form.quantity.data
        unit = form.unit.data

        # Check if ingredient already exists
        existing = MenuItemIngredient.query.filter_by(
            menu_item_id=menu_item_id,
            ingredient_id=ingredient_id
        ).first()

        if existing:
            # Update existing ingredient quantity and unit
            if menu_item.update_ingredient(ingredient_id, quantity, unit):
                flash("Ingredient updated successfully", "success")
            else:
                flash("Failed to update ingredient", "danger")
        else:
            # Add new ingredient
            if menu_item.add_ingredient(ingredient_id, quantity, unit):
                flash("Ingredient added successfully", "success")
            else:
                flash("Failed to add ingredient", "danger")

        return redirect(url_for("dashboard.manage_menu_item_ingredients", menu_item_id=menu_item_id))

    # Get all ingredients for current menu item
    current_ingredients = menu_item.get_ingredients()
    ingredient_quantities = {
        mi.ingredient_id: {'quantity': mi.quantity, 'unit': mi.unit}
        for mi in MenuItemIngredient.query.filter_by(menu_item_id=menu_item_id).all()
    }

    return render_template(
        "dashboard_menu_item_ingredients.html",
        menu_item=menu_item,
        form=form,
        current_ingredients=current_ingredients,
        ingredient_quantities=ingredient_quantities,
        pagetitle=f"Manage Ingredients - {menu_item.name}",
        menu_item_id=menu_item_id
    )

@dashboard.route("/menu_items/<int:menu_item_id>/ingredients/<int:ingredient_id>/delete", methods=["POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def delete_menu_item_ingredient(menu_item_id, ingredient_id):
    menu_item = MenuItem.get_by_id(menu_item_id)
    if not menu_item:
        flash("Menu item not found", "danger")
        return redirect(url_for("dashboard.menu_item_list"))

    if menu_item.remove_ingredient(ingredient_id):
        flash("Ingredient removed successfully", "success")
    else:
        flash("Failed to remove ingredient", "danger")

    return redirect(url_for("dashboard.manage_menu_item_ingredients", menu_item_id=menu_item_id))

# === Badge Management ===
@dashboard.route("/badges")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def badge_list():
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = WaterSavingBadge.query
    if search:
        query = query.filter(WaterSavingBadge.name.ilike(f"%{search}%"))
    
    badges = query.paginate(page=page, per_page=per_page)
    return render_template("dashboard_badges.html", items=badges, search=search)

@dashboard.route("/badges/add", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def add_badge():
    form = BadgeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            file = form.image.data
            filpath = current_app.config['UPLOAD_FOLDER'] + datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename
            
            WaterSavingBadge.create_badge(
                name=form.name.data,
                description=form.description.data,
                required_water_saved=form.required_water_saved.data,
                image_url=image_url
            )
            flash("Badge added successfully", "success")
            return redirect(url_for("dashboard.badge_list"))
    return render_template("dashboard_badge_add.html", form=form, pagetitle="Add Badge")

@dashboard.route("/badges/edit/<int:badge_id>", methods=["GET", "POST"])
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def edit_badge(badge_id):
    badge = WaterSavingBadge.get_badge_by_id(badge_id)
    if not badge:
        flash("Badge not found", "danger")
        return redirect(url_for("dashboard.badge_list"))
    
    form = BadgeForm(
        name=badge.name,
        description=badge.description,
        required_water_saved=badge.required_water_saved
    )
    
    if request.method == "POST":
        if form.validate_on_submit():
            file = form.image.data
            filpath = current_app.config['UPLOAD_FOLDER'] + datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename
            
            WaterSavingBadge.update_badge(
                badge_id=badge_id,
                name=form.name.data,
                description=form.description.data,
                required_water_saved=form.required_water_saved.data,
                image_url=image_url
            )
            flash("Badge updated successfully", "success")
            return redirect(url_for("dashboard.badge_list"))
    return render_template("dashboard_badge_edit.html", form=form, pagetitle="Edit Badge")

@dashboard.route("/badges/delete/<int:badge_id>")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value)
def delete_badge(badge_id):
    if WaterSavingBadge.delete_badge(badge_id):
        flash("Badge deleted successfully", "success")
    else:
        flash("Failed to delete badge", "danger")
    return redirect(url_for("dashboard.badge_list"))

@dashboard.route("/user_badges/<int:user_id>")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
def user_badges(user_id):
    badges = UserBadge.get_user_badges(user_id)
    return render_template("dashboard_user_badges.html", badges=badges, user_id=user_id)

@dashboard.route("/water_saving_history/<int:user_id>")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
def water_saving_history(user_id):
    history = UserWaterSavingHistory.get_user_history(user_id)
    return render_template("dashboard_water_saving_history.html", history=history, user_id=user_id)

@dashboard.route("/orders/<int:order_id>")
@dashboard_roles_required(Role.Admin.value, Role.Manager.value, Role.Staff.value)
def view_order(order_id):
    order = Order.query.options(
        joinedload(Order.customer),
        joinedload(Order.order_items).joinedload(OrderItem.menu_item)
    ).get_or_404(order_id)
    
    return render_template('dashboard_order_detail.html', order=order)
