# app/models.py
from datetime import datetime
from app import db
from app.models.order import Order
from sqlalchemy import Enum as SqlEnum
from app.common.MyEnum import Role
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.water_saving_badge import WaterSavingBadge

class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    role = db.Column(SqlEnum(Role), nullable=False)
    role_description = db.Column(db.String(255))
    story = db.Column(db.String(255))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contribution = db.Column(db.Numeric(10, 2), default=0) 
    image_url = db.Column(db.String(255))
    is_deleted = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum('active', 'inactive', name='status_enum'), default='active')
    address = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 添加与徽章的关系
    badges = db.relationship('WaterSavingBadge', secondary='UserBadges', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return str(self.user_id)

    @staticmethod
    def create_user(username, 
                    password_hash, 
                    email=None, 
                    phone_number=None, 
                    role='Customer', 
                    first_name=None, 
                    last_name=None, 
                    contribution=0,
                    image_url = None,
                    status='active'
                    ):
        new_user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            phone_number=phone_number,
            role=role,
            first_name=first_name,
            last_name=last_name,
            contribution=contribution,
            image_url = image_url,
            status=status
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user


    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()


    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

   
    
    @staticmethod
    def update_user(user_id, username=None, password_hash=None, email=None, phone_number=None, role=None, first_name=None, last_name=None, status=None, contribution=None, image_url=None, is_deleted=None):
        user = User.query.get(user_id)
        if user:
            if username:
                user.username = username
            if password_hash:
                user.password_hash = password_hash
            if email:
                user.email = email
            if phone_number:
                user.phone_number = phone_number
            if role:
                user.role = role
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if status:
                user.status = status
            if contribution:
                user.contribution = contribution
            if image_url:
                user.image_url = image_url
            if is_deleted:
                user.is_deleted = is_deleted
            user.updated_at = datetime.utcnow()  # Update modification time
            db.session.commit()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False


    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_users_by_status(status):
        return User.query.filter_by(status=status).all()

    def has_badge(self, badge_name):
        """Check if the user has a specified badge"""
        return any(badge.name == badge_name for badge in self.badges)

    def add_badge(self, badge_name):
        """Add a badge to the user"""
        badge = WaterSavingBadge.query.filter_by(name=badge_name).first()
        if badge and not self.has_badge(badge_name):
            self.badges.append(badge)
            db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()