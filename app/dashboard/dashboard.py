
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
from app.common.forms import MenuItemForm
from flask_wtf import FlaskForm
dashboard = Blueprint("dashboard", __name__, template_folder="templates")
# === Menu Item  ===
@dashboard.route("/")
def overview():
    user = current_user()
    print(app.config['UPLOAD_FOLDER'])
    name = "123"
    user = User.get_all_users()
    order = Order.get_all_orders()
    return render_template(f"dashboard_overview.html", name="name")

@dashboard.route("/menu_item_list", methods=["GET", "POST"])
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
def add_menu_item():
    if request.method == "POST":
        form = MenuItemForm()
        if form.validate_on_submit():
            MenuItem.create_menu_item(name=form.name.data, description=form.description.data, price=form.price.data, category=form.category.data, available=form.available.data, image_url=form.image_url.data)
            flash("Menu item added successfully", "success")
        return redirect(url_for("dashboard.menu_items_list"))
    return render_template("dashboard_add_menu_item.html")

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
    return render_template("dashboard_edit_menu_item.html", form=menu_item_form, image_url=menu_item.image_url, pagetitle="Edit "+ menu_item.name)

#create a new menu item
@dashboard.route("/menu_items/create", methods=["GET", "POST"])
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
    return render_template("dashboard_create_menu_item.html" , pagetitle=pagetitle, form=MenuItemForm())

@dashboard.route("/menu_items/delete/<int:menu_item_id>", methods=["GET"])
def delete_menu_item(menu_item_id):
    menu_item = MenuItem.get_by_id(menu_item_id)
    if not menu_item:
        flash("Menu item not found", "danger")
        return redirect(url_for("dashboard.menu_items_list"))
    MenuItem.delete(menu_item_id)
    flash("Menu item deleted successfully", "success")
    return redirect(url_for("dashboard.menu_items_list"))


@dashboard.route("/export_menu_items_csv")
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
        return Response(str(e), status=404)


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
# === Menu Item End ===

# === User Management ===
@dashboard.route("/users_list")
def users_list():
    # pagnation
    page = request.args.get('page', 1, type=int)
    per_page = 10
    users = User.query.paginate(page=page, per_page=per_page)
    return render_template("dashboard_users_list.html", items=users)

# === User Management End ===
@dashboard.route("/docs")
def docs():
    return render_template("docs.html")