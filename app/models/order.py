from datetime import datetime
from sqlalchemy import BigInteger, Enum
from sqlalchemy.orm import relationship
from app.extensions import db
from app.models.order_item import OrderItem
from app.models.payment import Payment


class Order(db.Model):
    __tablename__ = 'Orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=True) 
    order_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    status = db.Column(db.Enum('Pending', 'Preparing', 'Completed', 'Canceled', name='order_status_enum'), default='Pending')
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    recall_id = db.Column(BigInteger, nullable=True)  

    # Guest info fields
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.Text)
    city_or_town = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    email = db.Column(db.String(255))

    order_items = db.relationship('OrderItem', backref='order')
    payment = db.relationship('Payment', backref='order', uselist=False)
    customer = relationship('User', foreign_keys=[customer_id], backref='orders_as_customer')

    def __repr__(self):
        return f'<Order {self.order_id}>'

    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod
    def get_order_by_id(order_id):
        return Order.query.filter_by(order_id=order_id).first()

    @staticmethod
    def get_order_by_recall_id(recall_id):
        return Order.query.filter_by(recall_id=recall_id).first()
    
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.query.filter_by(customer_id=customer_id).all()

    @staticmethod
    def create_order(customer_id, total_amount, status='Pending', recall_id=None, 
                 first_name=None, last_name=None, address=None, city_or_town=None, zip_code=None, email=None):
        new_order = Order(
            customer_id=customer_id,
            total_amount=total_amount,
            status=status,
            recall_id=recall_id,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city_or_town=city_or_town,
            zip_code=zip_code,
            email=email
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order

    @staticmethod
    def update_order_status(order_id, new_status):
        order = Order.query.get(order_id)
        if order:
            order.status = new_status
            db.session.commit()
            return order
        return None

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False