# app/models.py
from datetime import datetime
from app.extensions import db
class Payment(db.Model):
    __tablename__ = 'Payments'

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    payment_method = db.Column(db.String(50))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f'<Payment {self.payment_id}>'
