# app/models.py
# app/models.py
from app import db
from datetime import datetime
from 

class MenuItem(db.Model):
    __tablename__ = 'MenuItems'

    menu_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50))
    available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    order_items = db.relationship('OrderItem', backref='menu_item')
    reviews = db.relationship('Review', backref='menu_item')

    def __repr__(self):
        return f'<MenuItem {self.name}>'
