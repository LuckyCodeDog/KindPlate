from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
# 创建数据库对象
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)

    from app.dashboard.dashboard import dashboard
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    from app.models.order import Order
    from app.models.user import User

    from app.models.order_item import OrderItem
    from app.models.menu_item import MenuItem
    from app.models.payment import Payment
    return app 
