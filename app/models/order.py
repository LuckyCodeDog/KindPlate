from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from app import db  # 假设 db 是全局数据库对象
from app.models.order_item import OrderItem
from app.models.payment import Payment
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
    @staticmethod
    def get_all_orders():
        return Order.query.all()
    # 静态方法 - 获取订单通过 ID
    @staticmethod
    def get_order_by_id(order_id):
        return Order.query.filter_by(order_id=order_id).first()

    # 静态方法 - 获取某个顾客的所有订单
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.query.filter_by(customer_id=customer_id).all()

    # 静态方法 - 获取某个服务员的所有订单
    @staticmethod
    def get_orders_by_waiter(waiter_id):
        return Order.query.filter_by(waiter_id=waiter_id).all()

    # 静态方法 - 创建一个新订单
    @staticmethod
    def create_order(customer_id, waiter_id, total_amount, status='Pending'):
        new_order = Order(customer_id=customer_id, waiter_id=waiter_id, total_amount=total_amount, status=status)
        db.session.add(new_order)
        db.session.commit()
        return new_order

    # 静态方法 - 更新订单状态
    @staticmethod
    def update_order_status(order_id, new_status):
        order = Order.query.get(order_id)
        if order:
            order.status = new_status
            db.session.commit()
            return order
        return None

    # 静态方法 - 删除订单
    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False
