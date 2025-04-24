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

    @staticmethod
    def get_all_order_items():
        return OrderItem.query.all()

    @staticmethod
    def get_order_items_by_order_id(order_id):
        return OrderItem.query.filter_by(order_id=order_id).all()

    @staticmethod
    def get_order_items_by_menu_item(menu_item_id):
        return OrderItem.query.filter_by(menu_item_id=menu_item_id).all()

    @staticmethod
    def create_order_item(order_id, menu_item_id, quantity, price):
        new_order_item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            price=price
        )
        db.session.add(new_order_item)
        db.session.commit()
        return new_order_item

    @staticmethod
    def update_order_item(order_item_id, quantity=None, price=None):
        order_item = OrderItem.query.get(order_item_id)
        if order_item:
            if quantity is not None:
                order_item.quantity = quantity
            if price is not None:
                order_item.price = price
            db.session.commit()
            return order_item
        return None

    @staticmethod
    def delete_order_item(order_item_id):
        order_item = OrderItem.query.get(order_item_id)
        if order_item:
            db.session.delete(order_item)
            db.session.commit()
            return True
        return False