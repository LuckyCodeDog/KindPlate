
from datetime import datetime
from enum import StrEnum
from app.extensions import db
from app.common.MyEnum import BookingStatus 
import uuid

class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    guests = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



    status = db.Column(db.Enum('pending', 'confirmed', 'cancelled', name='status_enum'), default='pending')

    reference_number = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    def __repr__(self):
        return f'<Booking {self.reference_number}>'

    @staticmethod
    def create(first_name, last_name, phone, email, guests, date, time, message=None, status=BookingStatus.PENDING.value):
        booking = Booking(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            guests=guests,
            date=date,
            time=time,
            message=message,
            status=status,
            reference_number=str(uuid.uuid4())
        )
        db.session.add(booking)
        try:
            db.session.commit()
            return booking
        except Exception as e:
            db.session.rollback()
            print("Create booking failed:", e)
            return None

    @staticmethod
    def get_all():
        return Booking.query.order_by(Booking.created_at.desc()).all()

    @staticmethod
    def get_by_id(booking_id):
        return Booking.query.get(booking_id)

    @staticmethod
    def get_by_reference(reference_number):
        return Booking.query.filter_by(reference_number=reference_number).first()

    @staticmethod
    def get_by_condition(**conditions):
        return Booking.query.filter_by(**conditions).all()

    @staticmethod
    def update(booking_id, **kwargs):
        booking = Booking.query.get(booking_id)
        if not booking:
            return None
        for key, value in kwargs.items():
            if hasattr(booking, key) and value is not None:
                setattr(booking, key, value)
        try:
            db.session.commit()
            return booking
        except Exception as e:
            db.session.rollback()
            print("Update booking failed:", e)
            return None

    @staticmethod
    def delete(booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return False
        try:
            db.session.delete(booking)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print("Delete booking failed:", e)
            return False
