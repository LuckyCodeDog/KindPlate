# app/models.py
from datetime import datetime
from app import db
from app.models.order import Order
from sqlalchemy import Enum as SqlEnum
from app.common.MyEnum import Role
from flask_login import UserMixin
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
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


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
            user.updated_at = datetime.utcnow()  # 更新修改时间
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