from app import db
from datetime import datetime

class UserBadge(db.Model):
    __tablename__ = 'UserBadges'
    
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('WaterSavingBadges.badge_id'), primary_key=True)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_user_badges(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def add_badge_to_user(cls, user_id, badge_id):
        user_badge = cls(user_id=user_id, badge_id=badge_id)
        db.session.add(user_badge)
        db.session.commit()
        return user_badge
    
    @classmethod
    def remove_badge_from_user(cls, user_id, badge_id):
        user_badge = cls.query.filter_by(user_id=user_id, badge_id=badge_id).first()
        if user_badge:
            db.session.delete(user_badge)
            db.session.commit()
            return True
        return False 