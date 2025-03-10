# app/models.py
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    role = db.Column(db.Enum('Admin', 'Waiter', 'Chef', 'Customer', name='role_enum'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    status = db.Column(db.Enum('active', 'inactive', name='status_enum'), default='active')
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = db.relationship('Order', backref='customer', foreign_keys='Order.customer_id')
    waiter_orders = db.relationship('Order', backref='waiter', foreign_keys='Order.waiter_id')
    reviews = db.relationship('Review', backref='customer')

    def __repr__(self):
        return f'<User {self.username}>'
