
import datetime
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app as app
from app.models.user import User
from app.models.order import Order
from app.models.menu_item import MenuItem
from app.common.login_required import login_required
from app.common.user import current_user
from app.common.forms import MenuItemForm
from flask_wtf import FlaskForm
dashboard = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard.route("/")
def overview():
    user = current_user()
    print(app.config['UPLOAD_FOLDER'])
    name = "123"
    user = User.get_all_users()
    order = Order.get_all_orders()
    print(order)
   # User.create_user(username="admin", password_hash="admin", email="123@123.com", phone_number="12345678901", role="Admin")
    print(user)
    return render_template(f"dashboard_overview.html", name="name")

@dashboard.route("/menu_item_list", methods=["GET", "POST"])
def menu_item_list():
    #if get 
    if request.method == "GET":
        page = request.args.get('page', 1, type=int)
        per_page = 10
        items = MenuItem.query.paginate(page=page, per_page=per_page)
        for item in items.items:
            print(item.menu_item_id)
        return render_template("dashboard_menu_items.html", items=items)
    return render_template("dashboard_menu_items.html")

@dashboard.route("/menu_items/add", methods=["GET", "POST"])
def add_menu_item():
    if request.method == "POST":
        form = MenuItemForm()
        if form.validate_on_submit():
            MenuItem.create_menu_item(name=form.name.data, description=form.description.data, price=form.price.data, category=form.category.data, available=form.available.data, image_url=form.image_url.data)
            flash("Menu item added successfully", "success")
        return redirect(url_for("dashboard.menu_items_list"))
    return render_template("dashboard_add_menu_item.html")
#test

@dashboard.route("/menu_items/edit/<int:menu_item_id>", methods=["GET", "POST"])
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
    return render_template("dashboard_edit_menu_item.html", form=menu_item_form, image_url=menu_item.image_url)


@dashboard.route("/docs")
def docs():
    return render_template("docs.html")