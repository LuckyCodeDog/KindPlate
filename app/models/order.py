# app/models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Order(db.Model):
    __tablename__ = 'Orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    waiter_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    order_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    status = db.Column(db.Enum('Pending', 'Preparing', 'Completed', 'Canceled', name='order_status_enum'), default='Pending')
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    order_items = db.relationship('OrderItem', backref='order')
    payment = db.relationship('Payment', backref='order', uselist=False)

    def __repr__(self):
        return f'<Order {self.order_id}>'
