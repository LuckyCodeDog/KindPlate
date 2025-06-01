from datetime import datetime
from flask import Blueprint, jsonify, session, send_from_directory, current_app
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
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.models.dto.cart_item_dto import cart_item_dto
from app.common.forms import BookingForm, CheckoutForm, RegisterForm, LoginForm, CustomerInfoForm
from flask_login import login_user, logout_user, current_user
from app.common.MyEnum import Role
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse
from app.common.login_required import roles_required
import os
from app.models.water_saving_badge import WaterSavingBadge
from app.models.user_water_saving_history import UserWaterSavingHistory
from werkzeug.utils import secure_filename
from decimal import Decimal
from app.models.payment import Payment
home = Blueprint("home", __name__, template_folder="templates")


@home.route("/")
def index():
    # load menu items limited to 10
    menu_items = MenuItem.query.limit(5).all()
    employees = User.query.filter(
        or_(
            User.role == Role.Manager,
            User.role == Role.Staff
        )
    ).limit(5).all()

    search = request.args.get('search', None)  
    page = request.args.get('page', 1, type=int)  
    per_page = 12  
    if search:
        items = MenuItem.query.filter(
                (MenuItem.name.ilike(f"%{search}%"))
            ).paginate(page=page, per_page=per_page)
    else:
        items = MenuItem.query.paginate(page=page, per_page=per_page)


    print(current_user.is_authenticated)
    return render_template("restaurant_index.html", employees=employees, menu_items=menu_items, search=search, items=items)

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

    # Calculate total items in cart
    cart_count = sum(item['quantity'] for item in cart)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        msg = f"{menu_item.name} has been added to your cart!"
        return jsonify({
            "message": msg,
            "cart_count": cart_count,
            "success": True
        })

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
    total_water_saved = 0

    for item in cart:
        menu_item = MenuItem.get_by_id(int(item['id']))
        if menu_item:
            quantity = item['quantity']
            menu_items.append(menu_item)
            total_price += menu_item.price * quantity

            # Calculate water saved for logged in users
            water_saved = 0
            if current_user.is_authenticated:
                # Get all ingredients for this menu item
                menu_item_ingredients = menu_item.ingredients.all()
                for menu_item_ingredient in menu_item_ingredients:
                    ingredient = menu_item_ingredient.ingredient
                    # If ingredient is meat-based, calculate water saved
                    if ingredient.meat_id:
                        # Convert quantity to kg for water usage calculation
                        quantity_in_kg = Decimal(str(menu_item_ingredient.quantity))
                        if menu_item_ingredient.unit == 'g':
                            quantity_in_kg /= Decimal('1000')
                        elif menu_item_ingredient.unit == 'l':
                            quantity_in_kg *= Decimal('1')  # 1L = 1kg
                        elif menu_item_ingredient.unit == 'gallon':
                            quantity_in_kg *= Decimal('3.78541')  # 1 gallon = 3.78541L
                        
                        # Calculate water saved (meat water usage - plant water usage)
                        water_saved += (ingredient.water_usage_l_per_kg - Decimal('0')) * quantity_in_kg * Decimal(str(quantity))
                total_water_saved += water_saved

            cart_item_dto_obj = cart_item_dto(
                menu_item_id=menu_item.menu_item_id,
                quantity=quantity,
                price=menu_item.price,
                name=menu_item.name,
                image_url=menu_item.image_url
            )
            cartItems.append(cart_item_dto_obj)
            
    # if guest 
    checkout_form = CheckoutForm()
    
    return render_template('restaurant_checkout.html', 
                         cartItems=cartItems, 
                         total_price=total_price, 
                         total_water_saved=total_water_saved,
                         form=checkout_form)


@home.route("/account", methods=["GET", "POST"])
def account():
    if current_user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'message': 'Already logged in',
                'redirect': url_for('home.index')
            })
        return redirect(url_for('home.index'))
    
    # Redirect to login page since we've separated the pages
    return redirect(url_for('home.login'))

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
#     session.pop('cart', None)  # Clear the cart in session

@home.route('/customer_info', methods=['GET', 'POST'])
@roles_required(Role.Customer.value,Role.Admin.value)
def customer_info():
    form = CustomerInfoForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.address = form.address.data
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.image_url = url_for('static', filename=f'uploads/{filename}')
        
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('home.customer_info'))
    
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.address.data = current_user.address
    
    # Get all badges
    all_badges = WaterSavingBadge.query.order_by(WaterSavingBadge.required_water_saved).all()
    
    # Get user's earned badges
    user_badges = current_user.badges
    
    # Calculate next available badge
    next_badge = None
    for badge in all_badges:
        if badge not in user_badges and current_user.contribution < badge.required_water_saved:
            next_badge = badge
            break
    
    # Calculate progress
    if next_badge:
        progress = (current_user.contribution / next_badge.required_water_saved) * 100
    else:
        progress = 100  # If all badges are earned, progress is 100%
    
    return render_template('restaurant_customer_info.html', 
                         form=form, 
                         all_badges=all_badges,
                         user_badges=user_badges,
                         next_badge=next_badge,
                         progress=progress)

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
        
        # Email validation
        email = data.get('email', '')
        if email:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                return jsonify(success=False, message="Please enter a valid email address"), 400
        
        # Phone validation
        phone = data.get('phone', '')
        phone_pattern = r'^\+?1?\d{9,15}$'  # Allows international format
        if not re.match(phone_pattern, phone):
            return jsonify(success=False, message="Please enter a valid phone number (9-15 digits)"), 400
        
        booking_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        booking_time = datetime.strptime(data['time'], "%H:%M").time()
        
        # Validate if booking date is in the future
        today = datetime.now().date()
        if booking_date < today:
            return jsonify(success=False, message="Booking date must be today or later"), 400
            
        # If booking is for today, validate the time
        if booking_date == today:
            current_time = datetime.now().time()
            if booking_time <= current_time:
                return jsonify(success=False, message="Booking time must be later than current time for today's bookings"), 400
        
        new_booking = Booking.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=phone,
            email=email,
            guests=int(data['guests']),
            date=booking_date,
            time=booking_time,
            message=data.get('message'),
        )
        return jsonify(success=True, reference_number=new_booking.reference_number), 200
    except Exception as e:
        print("Error creating booking:", e)
        return jsonify(success=False, message="Failed to create booking"), 500

  


@home.route("/menu_items", methods=["GET", "POST"])
def menu():
    if request.method == "GET":
        search = request.args.get('search', None)  
        page = request.args.get('page', 1, type=int)  
        per_page = 12  
        if search:
            items = MenuItem.query.filter(
                (MenuItem.name.ilike(f"%{search}%"))
            ).paginate(page=page, per_page=per_page)
        else:
            items = MenuItem.query.paginate(page=page, per_page=per_page)

        return render_template("restaurant_menu.html", items=items, search=search)

@home.route('/download-menu')
def download_menu():
    """Download the restaurant menu PDF."""
    try:
        return send_from_directory(
            directory=os.path.join(current_app.root_path, 'static', 'download'),
            path='menu.pdf',
            as_attachment=True,
            download_name='restaurant_menu.pdf'
        )
    except Exception as e:
        flash('Error downloading menu. Please try again later.', 'error')
        return redirect(url_for('home.restaurant_menu'))


# pagination for team
@home.route('/team')
def team():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    items = User.query.filter(
        User.role == Role.Manager.value or User.role == Role.Staff.value
    ).paginate(page=page, per_page=per_page)
    return render_template('restaurant_team.html', items=items)

@home.route('/process_payment', methods=['POST'])
def process_payment():
    cart = session.get('cart', [])
    if not cart:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"error": "Your cart is empty"}), 400
        flash('Your cart is empty!')
        return redirect(url_for('home.view_cart'))
        
    try:
        # Calculate total price
        total_price = 0
        order_items = []
        
        for item in cart:
            menu_item = MenuItem.get_by_id(int(item['id']))
            if menu_item:
                quantity = item['quantity']
                total_price += menu_item.price * quantity
                
                order_items.append({
                    'menu_item': menu_item,
                    'quantity': quantity,
                    'price': menu_item.price
                })
        
        # Create new order
        new_order = Order(
            customer_id=current_user.user_id if current_user.is_authenticated else None,
            total_amount=total_price,
            status='Pending',
            order_date=datetime.now(),
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            address=request.form.get('address'),
            city_or_town=request.form.get('city'),
            zip_code=request.form.get('zip_code'),
            email=request.form.get('email')
        )
        db.session.add(new_order)
        db.session.flush()  # Get the order ID
        
        # Add order items
        for item in order_items:
            order_item = OrderItem(
                order_id=new_order.order_id,
                menu_item_id=item['menu_item'].menu_item_id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        
        # Create payment record
        payment = Payment(
            order_id=new_order.order_id,
            payment_method=request.form.get('payment_method'),
            amount=total_price
        )
        db.session.add(payment)
        
        # Update user's contribution if logged in
        if current_user.is_authenticated:
            # Calculate water saved based on ingredients
            total_water_saved = 0
            for item in order_items:
                menu_item = item['menu_item']
                quantity = item['quantity']
                
                # Get all ingredients for this menu item
                menu_item_ingredients = menu_item.ingredients.all()
                for menu_item_ingredient in menu_item_ingredients:
                    ingredient = menu_item_ingredient.ingredient
                    # If ingredient is meat-based, calculate water saved
                    if ingredient.meat_id:
                        # Convert quantity to kg for water usage calculation
                        quantity_in_kg = Decimal(str(menu_item_ingredient.quantity))
                        if menu_item_ingredient.unit == 'g':
                            quantity_in_kg /= Decimal('1000')
                        elif menu_item_ingredient.unit == 'l':
                            quantity_in_kg *= Decimal('1')  # 1L = 1kg
                        elif menu_item_ingredient.unit == 'gallon':
                            quantity_in_kg *= Decimal('3.78541')  # 1 gallon = 3.78541L
                        
                        # Calculate water saved (meat water usage - plant water usage)
                        water_saved = (ingredient.water_usage_l_per_kg - Decimal('0')) * quantity_in_kg * Decimal(str(quantity))
                        total_water_saved += water_saved
            
            # Update user's contribution
            current_user.contribution += total_water_saved
            
            # Record water saving history
            history = UserWaterSavingHistory(
                user_id=current_user.user_id,
                order_id=new_order.order_id,
                water_saved=total_water_saved
            )
            db.session.add(history)
            
            # Check and award badges based on total contribution
            badge_thresholds = {
                'Sprout Starter': 50.00,
                'Aqua Guardian': 200.00,
                'Water Warrior': 500.00,
                'Eco Ripple Master': 1000.00,
                'Planet Paladin': 2000.00,
                'Sustainability Sage': 5000.00,
                'KindPlate Legend': 10000.00
            }
            
            for badge_name, threshold in badge_thresholds.items():
                if current_user.contribution >= threshold and not current_user.has_badge(badge_name):
                    badge = WaterSavingBadge.get_badge_by_name(badge_name)
                    if badge:
                        current_user.add_badge(badge_name)
                        history.badge_id = badge.badge_id
        
        # Commit the transaction
        db.session.commit()
        
        # Clear the cart
        session.pop('cart', None)
        
        # If it's an AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            response_data = {
                "success": True,
                "message": "Order placed successfully!",
                "order_id": new_order.order_id,
                "total_amount": float(total_price)
            }
            
            # Add water saved info only for logged in users
            if current_user.is_authenticated:
                response_data.update({
                    "water_saved": float(total_water_saved),
                    "new_contribution": float(current_user.contribution)
                })
            
            return jsonify(response_data)
        
        # For regular form submission, redirect to order confirmation
        flash('Order placed successfully!', 'success')
        if current_user.is_authenticated:
            return redirect(url_for('home.order_confirmation', order_id=new_order.order_id))
        else:
            return redirect(url_for('home.order_confirmation', 
                                  order_id=new_order.order_id,
                                  email=new_order.email))
        
    except Exception as e:
        db.session.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"error": str(e)}), 500
        flash(f'Error processing payment: {str(e)}', 'error')
        return redirect(url_for('home.checkout'))

@home.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    
    # For logged-in users, check if they own the order
    if current_user.is_authenticated:
        if order.customer_id != current_user.user_id:
            flash("You don't have permission to view this order", "danger")
            return redirect(url_for('home.index'))
    # For guest users, check if the email matches
    else:
        if not order.email or order.email != request.args.get('email'):
            flash("Please provide the email address used for this order", "warning")
            return redirect(url_for('home.checkout'))
    
    # Get water saving information if the user is logged in
    water_saved = None
    if current_user.is_authenticated:
        water_saving_history = UserWaterSavingHistory.query.filter_by(
            order_id=order.order_id,
            user_id=current_user.user_id
        ).first()
        if water_saving_history:
            water_saved = water_saving_history.water_saved
        
    return render_template('restaurant_order_confirmation.html', 
                         order=order, 
                         water_saved=water_saved)

@home.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter(
            (User.username == login_form.username_or_email.data) | 
            (User.email == login_form.username_or_email.data)
        ).first()
        
        if user and check_password_hash(user.password_hash, login_form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('home.index')
            return redirect(next_page)
        else:
            flash('Invalid username/email or password', 'danger')
    
    return render_template('restaurant_login.html', login_form=login_form)

@home.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        try:
            # Check if username already exists
            if User.query.filter_by(username=register_form.username.data).first():
                return render_template('restaurant_register.html', register_form=register_form)
            
            # Check if email already exists
            if User.query.filter_by(email=register_form.email.data).first():
                return render_template('restaurant_register.html', register_form=register_form)
            
            # Create new user
            user = User(
                username=register_form.username.data,
                first_name=register_form.first_name.data,
                last_name=register_form.last_name.data,
                email=register_form.email.data,
                phone_number=register_form.phone_number.data,
                role=Role.Customer.value,  # Set default role as Customer
                password_hash=generate_password_hash(register_form.password.data)  # Set password hash directly
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Automatically log in the user after successful registration
            login_user(user)
            flash('Registration successful! Welcome to KindPlate.', 'success')
            return redirect(url_for('home.index'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Registration error: {str(e)}')
            current_app.logger.error(f'Form data: {register_form.data}')
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('restaurant_register.html', register_form=register_form)
    
    # If form validation fails, show the errors
    if request.method == 'POST':
        for field, errors in register_form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    
    return render_template('restaurant_register.html', register_form=register_form)
