# app/models.py
from datetime import datetime
from app import db
class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    role = db.Column(db.Enum('Admin', 'Waiter', 'Chef', 'Customer', name='role_enum'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    status = db.Column(db.Enum('active', 'inactive', name='status_enum'), default='active')
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = db.relationship('Order', backref='customer', foreign_keys='Order.customer_id')

    def __repr__(self):
        return f'<User {self.username}>'
      # 静态方法：创建用户
    @staticmethod
    def create_user(username, password_hash, email=None, phone_number=None, role='Customer', first_name=None, last_name=None):
        new_user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            phone_number=phone_number,
            role=role,
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    # 静态方法：根据用户名获取用户
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    # 静态方法：根据用户ID获取用户
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    # 静态方法：更新用户信息
    @staticmethod
    def update_user(user_id, username=None, password_hash=None, email=None, phone_number=None, role=None, first_name=None, last_name=None, status=None):
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
            user.updated_at = datetime.utcnow()  # 更新修改时间
            db.session.commit()
            return user
        return None

    # 静态方法：删除用户
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    # 静态方法：获取所有用户
    @staticmethod
    def get_all_users():
        return User.query.all()

    # 静态方法：根据状态获取用户
    @staticmethod
    def get_users_by_status(status):
        return User.query.filter_by(status=status).all()