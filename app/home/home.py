from flask import Blueprint, session
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from sqlalchemy import or_
from app import db
from app.common.MyEnum import Role
from app.models.user import User
from app.models.order import Order
from app.models.menu_item import MenuItem
from app.common.login_required import login_required
from app.common.user import current_user  



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
    return render_template("restaurant_index.html", employees=employees, menu_items=menu_items)

@home.route("/add_to_cart/<int:menu_item_id>", methods=["POST"])
def add_to_cart(menu_item_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']

    menu_item_id_str = str(menu_item_id)

    if menu_item_id_str in cart:
        cart[menu_item_id_str] += 1
    else:
        cart[menu_item_id_str] = 1

    session['cart'] = cart
    return redirect(url_for("home.index"))

@home.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    menu_items = MenuItem.query.filter(MenuItem.id.in_(cart.keys())).all()
    total_price = sum(item.price * cart[item.id] for item in menu_items)
    
    print("Cart contents:", menu_items)
    return render_template("cart.html", menu_items=menu_items, cart=cart, total_price=total_price)
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
