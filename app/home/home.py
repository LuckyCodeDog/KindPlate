from datetime import datetime
from flask import Blueprint, jsonify, session
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from sqlalchemy import or_
from app import db
from flask import current_app as app
from app.common.MyEnum import BookingStatus, Role
from app.common.salt import password_salt
from app.models.booking import Booking
from app.models.user import User
from app.models.order import Order
from app.models.menu_item import MenuItem
from app.models.dto.cart_item_dto import cart_item_dto
from app.common.forms import BookingForm, CheckoutForm, RegisterForm, LoginForm, CustomerInfoForm
from flask_login import login_user, logout_user, current_user
from app.common.MyEnum import Role
from werkzeug.security import generate_password_hash, check_password_hash
from app.common.login_required import roles_required
home = Blueprint("home", __name__, template_folder="templates")


@home.route("/")
def index():
    # load menu items limited to 10
    menu_items = MenuItem.query.limit(5).all()
    employees = User.query.filter(
        or_(
            User.role == Role.Waiter,
            User.role == Role.Chef
        )
    ).limit(5).all()
    print(current_user.is_authenticated)
    return render_template("restaurant_index.html", employees=employees, menu_items=menu_items)

@home.route("/add_to_cart/<int:menu_item_id>", methods=["POST"])
def add_to_cart(menu_item_id):
    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']
    menu_item_id_str = str(menu_item_id)

    found = False
    for item in cart:
        if item['id'] == menu_item_id_str:
            item['quantity'] += 1
            found = True
            break

    if not found:
        cart.append({'id': menu_item_id_str, 'quantity': 1})

    session['cart'] = cart

    menu_item = MenuItem.query.get(menu_item_id)
    print(menu_item)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        msg = f"{menu_item.name} has been added to your cart!"
        return jsonify({"message": msg})

    flash("Item added to cart!")
    return redirect(request.referrer or url_for("home.index"))


@home.route("/cart")
def view_cart():
    cart = session.get("cart", [])
    print("Cart:", cart)

    if not cart:
        return render_template("restaurant_cart.html", cartItems=[], total_price=0)

    menu_items = []
    cartItems = []
    total_price = 0

    for item in cart:
        menu_item = MenuItem.get_by_id(int(item['id']))
        if menu_item:
            quantity = item['quantity']
            menu_items.append(menu_item)
            total_price += menu_item.price * quantity

            cart_item_dto_obj = cart_item_dto(
                menu_item_id=menu_item.menu_item_id,
                quantity=quantity,
                price=menu_item.price,
                name=menu_item.name,
                image_url=menu_item.image_url
            )
            print(str(cart_item_dto_obj.image_url))
            cartItems.append(cart_item_dto_obj)
    
    print("Cart contents:", cartItems)
    return render_template("restaurant_cart.html", cartItems=cartItems, total_price=total_price)


#update the cart
@home.route('/update_cart', methods=['POST'])
def update_cart():
    cart_data = request.json.get('cart')
    #validate the cart data
    print(cart_data)
    if not cart_data:
        return jsonify({"error": "Invalid cart data"}), 400
    # validate the cart data in db
    for data in cart_data:
        print(data)
        menu_item = MenuItem.query.get(int(data["id"]))
        if not menu_item:
            return jsonify({"error": f"Some Menu item with ids  does not exist"}), 400
    #update the session cart
    session['cart'] = cart_data
    flash('Your cart has been updated!')
    return jsonify({"message": "Cart updated successfully!"})


#check out the cart
@home.route('/checkout', methods=['GET'])
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash('Your cart is empty!')
        return redirect(url_for('home.view_cart'))

    menu_items = []
    cartItems = []
    total_price = 0
    for item in cart:
        menu_item = MenuItem.get_by_id(int(item['id']))
        if menu_item:
            quantity = item['quantity']
            menu_items.append(menu_item)
            total_price += menu_item.price * quantity

            cart_item_dto_obj = cart_item_dto(
                menu_item_id=menu_item.menu_item_id,
                quantity=quantity,
                price=menu_item.price,
                name=menu_item.name,
                image_url=menu_item.image_url
            )
            print(str(cart_item_dto_obj.image_url))
            cartItems.append(cart_item_dto_obj)
            
    # if guest 
    checkout_form = CheckoutForm()
    
    return render_template('restaurant_checkout.html', cartItems=cartItems, total_price=total_price, form=checkout_form)


@home.route("/account", methods=["GET", "POST"])
def account():
    login_form = LoginForm()

    register_form = RegisterForm()

    if request.method == "POST":
        if login_form.submit.data and login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username_or_email.data).first()
            if user and check_password_hash(user.password_hash, login_form.password.data):
                login_user(user)
                flash(f"Login successful, welcome !", "success")
                return redirect(url_for("home.index"))
            else:
                flash("Invalid credentials", "danger")

        print(register_form.validate_on_submit())
        flag = register_form.validate_on_submit()
        if register_form.submit.data and register_form.validate_on_submit():
            if User.query.filter_by(username=register_form.username.data).first():
                flash("Username already exists", "danger")
            else:
                user = User.create_user(
                    username=register_form.username.data,
                    email=register_form.email.data,
                    password_hash=generate_password_hash(register_form.password.data),
                    role=Role.Customer.value, 
                    first_name=register_form.first_name.data,
                    last_name=register_form.last_name.data
                )
                login_user(user)
                flash("Registration successful", "success")
                return redirect(url_for("home.index"))
    return render_template("restaurant_account.html", login_form=login_form, register_form=register_form)

#logout the user
@home.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home.index"))

# def merge_session_cart_to_db(user_id):
#     session_cart = session.get('cart', {})
#     for product_id_str, quantity in session_cart.items():
#         product_id = int(product_id_str)
        
#       
#         item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
#         if item:
#             item.quantity += quantity
#         else:
#             item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
#             db.session.add(item)
#     db.session.commit()
#     session.pop('cart', None)  # 清空 session 中的购物车

@home.route('/customer_info', methods=['GET', 'POST'])
@roles_required(Role.Customer.value)
def customer_info():
    customerform = CustomerInfoForm()
    if request.method == 'POST' and customerform.validate_on_submit():
        # Get the form data
        first_name = customerform.first_name.data
        last_name = customerform.last_name.data
        email = customerform.email.data
        phone = customerform.phone_number.data
        contribution = customerform.contribution.data
        address = customerform.address.data
        # save the image if provided
        image = customerform.image.data
        if image:
            # Save the image to the server and get the URL
            file = customerform.image.data
            filpath = app.config['UPLOAD_FOLDER'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+file.filename
            file.save(filpath)
            image_url = url_for('static', filename='uploads/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + file.filename 
            current_user.image_url = image_url

        # Update the current user's information
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email
        current_user.phone_number = phone

        # Commit the changes to the database
        db.session.commit()
        flash('Your information has been updated!', 'success')
        return redirect(url_for('home.customer_info'))
    customerform.first_name.data = current_user.first_name
    customerform.last_name.data = current_user.last_name
    customerform.email.data = current_user.email
    customerform.phone_number.data = current_user.phone_number
    customerform.contribution.data = current_user.contribution
    return render_template('restaurant_customer_info.html', user=current_user, form=customerform)

#blog 
@home.route('/blog')
def blog():
    return render_template('restaurant_blog.html')

#blog details
@home.route('/blog/<int:blog_id>')
def blog_details(blog_id):
    # Fetch the blog post from the database using the blog_id
    # For now, we'll just return a placeholder template
    return render_template('restaurant_blog_details.html', blog_id=blog_id)


#about us
@home.route('/about')
def about():
    return render_template('restaurant_about.html')

@home.route('/booking', methods=['POST'])
def book():
    try:
        data = request.form
        new_booking = Booking.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            email=data.get('email'),
            guests=int(data['guests']),
            date=datetime.strptime(data['date'], "%Y-%m-%d").date(),
            time=datetime.strptime(data['time'], "%H:%M").time(),
            message=data.get('message'),
        )
        return jsonify(success=True, reference_number=new_booking.reference_number), 200
    except Exception as e:
        print("Error creating booking:", e)
        return jsonify(success=False, message="Failed to create booking"), 500

  