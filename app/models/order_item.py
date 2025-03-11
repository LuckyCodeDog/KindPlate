# app/models.py
from app import db

class OrderItem(db.Model):
    __tablename__ = 'OrderItems'

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('MenuItems.menu_item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.order_item_id}>'
