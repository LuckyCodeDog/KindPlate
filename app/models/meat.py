from datetime import datetime
from app.extensions import db

class Meat(db.Model):
    __tablename__ = 'Meats'

    meat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meat_type = db.Column(db.Enum('Chicken', 'Duck', 'Fish', 'Pork', 'Beef', 'Egg'), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f'<Meat {self.meat_type}>'

    @staticmethod
    def create(meat_type, description=None):
        meat = Meat(
            meat_type=meat_type,
            description=description
        )
        db.session.add(meat)
        try:
            db.session.commit()
            return meat
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def get_all():
        return Meat.query.all()

    @staticmethod
    def get_by_id(meat_id):
        return Meat.query.get(meat_id)

    @staticmethod
    def update(meat_id, meat_type=None, description=None):
        meat = Meat.query.get(meat_id)
        if not meat:
            return None

        if meat_type:
            meat.meat_type = meat_type
        if description is not None:
            meat.description = description

        try:
            db.session.commit()
            return meat
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def delete(meat_id):
        meat = Meat.query.get(meat_id)
        if not meat:
            return False
        try:
            db.session.delete(meat)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False 