from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from app import db
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
    user = current_user()
    return render_template("restaurant_index.html", user=user, menu_items=menu_items)


# def merge_session_cart_to_db(user_id):
#     session_cart = session.get('cart', {})
#     for product_id_str, quantity in session_cart.items():
#         product_id = int(product_id_str)
        
#         # 查询是否已在数据库中
#         item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
#         if item:
#             item.quantity += quantity
#         else:
#             item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
#             db.session.add(item)
#     db.session.commit()
#     session.pop('cart', None)  # 清空 session 中的购物车
