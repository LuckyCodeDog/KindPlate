import os
from flask import Flask
from config import Config
from app.extensions import db, login_manager
from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_random_generated_secret_key'
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads/'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['WTF_CSRF_ENABLED'] = False
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    from app.dashboard.dashboard import dashboard
    from app.home.home import home
    
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(home, url_prefix='/')
    from app.models.order import Order
    from app.models.user import User
    from app.models.order_item import OrderItem
    from app.models.menu_item import MenuItem
    from app.models.payment import Payment
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    return app 
