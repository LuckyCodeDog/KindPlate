from datetime import datetime
from app.extensions import db

class Ingredient(db.Model):
    __tablename__ = 'Ingredients'

    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    meat_id = db.Column(db.Integer, db.ForeignKey('Meats.meat_id'))
    water_usage_l_per_kg = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    # Relationships
    meat = db.relationship('Meat', backref='ingredients')

    def __repr__(self):
        return f'<Ingredient {self.name}>'

    @staticmethod
    def create(name, description=None, meat_id=None, water_usage_l_per_kg=0):
        ingredient = Ingredient(
            name=name,
            description=description,
            meat_id=meat_id,
            water_usage_l_per_kg=water_usage_l_per_kg
        )
        db.session.add(ingredient)
        try:
            db.session.commit()
            return ingredient
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def get_all():
        return Ingredient.query.all()

    @staticmethod
    def get_by_id(ingredient_id):
        return Ingredient.query.get(ingredient_id)

    @staticmethod
    def update(ingredient_id, name=None, description=None, meat_id=None, water_usage_l_per_kg=None):
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return None
        
        if name:
            ingredient.name = name
        if description is not None:
            ingredient.description = description
        if meat_id is not None:
            ingredient.meat_id = meat_id
        if water_usage_l_per_kg is not None:
            ingredient.water_usage_l_per_kg = water_usage_l_per_kg
        
        try:
            db.session.commit()
            return ingredient
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def delete(ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return False
        try:
            db.session.delete(ingredient)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False 