from app import db
from datetime import datetime
from sqlalchemy import Numeric

class WaterSavingBadge(db.Model):
    __tablename__ = 'WaterSavingBadges'
    
    badge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    required_water_saved = db.Column(Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_badges = db.relationship('UserBadge', backref='badge', lazy=True)
    water_saving_history = db.relationship('UserWaterSavingHistory', lazy=True)
    
    @classmethod
    def get_all_badges(cls):
        return cls.query.all()
    
    @classmethod
    def get_badge_by_id(cls, badge_id):
        return cls.query.get(badge_id)
    
    @classmethod
    def get_badge_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def create_badge(cls, name, description, required_water_saved, image_url=None):
        badge = cls(
            name=name,
            description=description,
            required_water_saved=required_water_saved,
            image_url=image_url
        )
        db.session.add(badge)
        db.session.commit()
        return badge
    
    @classmethod
    def update_badge(cls, badge_id, name=None, description=None, required_water_saved=None, image_url=None):
        badge = cls.get_badge_by_id(badge_id)
        if badge:
            if name:
                badge.name = name
            if description:
                badge.description = description
            if required_water_saved:
                badge.required_water_saved = required_water_saved
            if image_url:
                badge.image_url = image_url
            db.session.commit()
            return badge
        return None
    
    @classmethod
    def delete_badge(cls, badge_id):
        badge = cls.get_badge_by_id(badge_id)
        if badge:
            db.session.delete(badge)
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return f'<WaterSavingBadge {self.name}>' 