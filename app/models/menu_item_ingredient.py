from app.extensions import db
from app.models.menu_item import MenuItem
from app.models.ingredient import Ingredient

class MenuItemIngredient(db.Model):
    __tablename__ = 'MenuItemIngredients'

    menu_item_id = db.Column(db.Integer, db.ForeignKey('MenuItems.menu_item_id', ondelete='CASCADE'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredients.ingredient_id', ondelete='CASCADE'), primary_key=True)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    unit = db.Column(db.Enum('l', 'g', 'kg', 'gallon'), nullable=False)

    # Relationships
    menu_item = db.relationship('MenuItem', backref=db.backref('ingredients', lazy='dynamic', cascade="all, delete-orphan"))
    ingredient = db.relationship('Ingredient', backref=db.backref('menu_items', lazy='dynamic', cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<MenuItemIngredient {self.menu_item_id}:{self.ingredient_id}>'

    @staticmethod
    def create(menu_item_id, ingredient_id, quantity, unit):
        menu_item_ingredient = MenuItemIngredient(
            menu_item_id=menu_item_id,
            ingredient_id=ingredient_id,
            quantity=quantity,
            unit=unit
        )
        db.session.add(menu_item_ingredient)
        try:
            db.session.commit()
            return menu_item_ingredient
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def get_by_menu_item(menu_item_id):
        return MenuItemIngredient.query.filter_by(menu_item_id=menu_item_id).all()

    @staticmethod
    def update(menu_item_id, ingredient_id, quantity=None, unit=None):
        menu_item_ingredient = MenuItemIngredient.query.filter_by(
            menu_item_id=menu_item_id,
            ingredient_id=ingredient_id
        ).first()
        
        if not menu_item_ingredient:
            return None

        if quantity is not None:
            menu_item_ingredient.quantity = quantity
        if unit is not None:
            menu_item_ingredient.unit = unit

        try:
            db.session.commit()
            return menu_item_ingredient
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def delete(menu_item_id, ingredient_id):
        menu_item_ingredient = MenuItemIngredient.query.filter_by(
            menu_item_id=menu_item_id,
            ingredient_id=ingredient_id
        ).first()
        
        if not menu_item_ingredient:
            return False

        try:
            db.session.delete(menu_item_ingredient)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    def calculate_water_usage(self):
        """计算该原材料的用水量"""
        # 获取原材料的每千克用水量
        water_usage_per_kg = float(self.ingredient.water_usage_l_per_kg)
        
        # 根据单位转换数量到千克
        quantity_in_kg = float(self.quantity)
        if self.unit == 'g':
            quantity_in_kg /= 1000
        elif self.unit == 'l':
            quantity_in_kg *= 1  # 假设1升水等于1千克
        elif self.unit == 'gallon':
            quantity_in_kg *= 3.78541  # 1加仑 = 3.78541升
        
        return quantity_in_kg * water_usage_per_kg 