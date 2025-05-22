from app import db
from datetime import datetime

class UserWaterSavingHistory(db.Model):
    __tablename__ = 'UserWaterSavingHistory'
    
    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'))
    water_saved = db.Column(db.DECIMAL(10,2), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('WaterSavingBadges.badge_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_user_history(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def add_history(cls, user_id, order_id, water_saved, badge_id=None):
        history = cls(
            user_id=user_id,
            order_id=order_id,
            water_saved=water_saved,
            badge_id=badge_id
        )
        db.session.add(history)
        db.session.commit()
        return history 