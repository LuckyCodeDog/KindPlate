from app import db
from datetime import datetime

class WaterSavingBadge(db.Model):
    __tablename__ = 'WaterSavingBadges'
    
    badge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    required_water_saved = db.Column(db.DECIMAL(10,2), nullable=False)
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
    def create_badge(cls, name, description, required_water_saved, image_url):
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
    def update_badge(cls, badge_id, **kwargs):
        badge = cls.get_badge_by_id(badge_id)
        if badge:
            for key, value in kwargs.items():
                setattr(badge, key, value)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def delete_badge(cls, badge_id):
        badge = cls.get_badge_by_id(badge_id)
        if badge:
            db.session.delete(badge)
            db.session.commit()
            return True
        return False 