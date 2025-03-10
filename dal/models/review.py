# app/models.py
from app import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'Reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('MenuItems.menu_item_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    review_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.review_id}>'
