from app import db
from datetime import datetime

class UserWaterSavingHistory(db.Model):
    __tablename__ = 'UserWaterSavingHistory'

    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'))
    water_saved = db.Column(db.Numeric(10, 2), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('WaterSavingBadges.badge_id'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    # 关系
    user = db.relationship('User', backref=db.backref('water_saving_history', lazy='dynamic'))
    order = db.relationship('Order', backref=db.backref('water_saving_history', lazy='dynamic'))
    badge = db.relationship('WaterSavingBadge', backref=db.backref('awarded_history', lazy='dynamic'))

    def __repr__(self):
        return f'<UserWaterSavingHistory {self.history_id}>' 