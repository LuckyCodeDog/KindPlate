from datetime import datetime
from app.extensions import db

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
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='menu_item')

    def __repr__(self):
        return f'<MenuItem {self.name}>'

    @staticmethod
    def create(name, description, price, category=None, available=True, image_url=None):
        menu_item = MenuItem(
            name=name,
            description=description,
            price=price,
            category=category,
            available=available,
            image_url=image_url
        )
        db.session.add(menu_item)
        try:
            db.session.commit()
            return menu_item
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def get_all():
        return MenuItem.query.all()

    @staticmethod
    def get_by_id(menu_item_id):
        return MenuItem.query.get(menu_item_id)

    @staticmethod
    def get_by_condition(**conditions):
        return MenuItem.query.filter_by(**conditions).all()

    @staticmethod
    def update(menu_item_id, name=None, description=None, price=None, category=None, available=None, image_url=None):
        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            return None
        if name:
            menu_item.name = name
        if description:
            menu_item.description = description
        if price is not None:
            menu_item.price = price
        if category:
            menu_item.category = category
        if available is not None:
            menu_item.available = available
        if image_url:
            menu_item.image_url = image_url
        try:
            db.session.commit()
            return menu_item
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def delete(menu_item_id):
        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            return False
        try:
            db.session.delete(menu_item)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    # New ingredient-related methods
    def get_ingredients(self):
        """獲取菜品的所有原材料"""
        return [item.ingredient for item in self.ingredients]

    def add_ingredient(self, ingredient_id, quantity, unit):
        """添加原材料到菜品"""
        from app.models.menu_item_ingredient import MenuItemIngredient
        return MenuItemIngredient.create(
            menu_item_id=self.menu_item_id,
            ingredient_id=ingredient_id,
            quantity=quantity,
            unit=unit
        )

    def update_ingredient(self, ingredient_id, quantity=None, unit=None):
        """更新菜品中的原材料信息"""
        from app.models.menu_item_ingredient import MenuItemIngredient
        return MenuItemIngredient.update(
            menu_item_id=self.menu_item_id,
            ingredient_id=ingredient_id,
            quantity=quantity,
            unit=unit
        )

    def remove_ingredient(self, ingredient_id):
        """從菜品中移除原材料"""
        from app.models.menu_item_ingredient import MenuItemIngredient
        return MenuItemIngredient.delete(
            menu_item_id=self.menu_item_id,
            ingredient_id=ingredient_id
        )
