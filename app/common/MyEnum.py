from enum import Enum

class Role(Enum):
    Admin = 'admin'
    Manager = 'manager'
    Staff = 'staff'
    Customer = 'customer'


class OrderStatus(Enum):
    Pending = "Pending"
    Preparing = "Preparing"
    Completed = "Completed"
    Canceled = "Canceled"
    
class MeatType(Enum):
    Chicken = 'Chicken'
    Duck = 'Duck'
    Fish = 'Fish'
    Pork = 'Pork'
    Beef = 'Beef'
    Egg = 'Egg'
    
class UserStatus(Enum):
    Active = 'Active'
    Inactive = 'Inactive'
    
class PaymentMethod(Enum):
    CARD = "card"
    PAYPAL = "paypal"
    CASH = "cash"

class BookingStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"