from app.extensions import db

# First, import models without relationships
from app.models.meat import Meat

# Then import models with relationships in correct order
from app.models.menu_item import MenuItem
from app.models.ingredient import Ingredient
from app.models.menu_item_ingredient import MenuItemIngredient

# Import other models
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.booking import Booking
from app.models.restaurant_profile import RestaurantProfile
from app.models.water_saving_badge import WaterSavingBadge
from app.models.user_water_saving_history import UserWaterSavingHistory

# Initialize all relationships
__all__ = [
    'Meat',
    'MenuItem',
    'Ingredient',
    'MenuItemIngredient',
    'User',
    'Order',
    'OrderItem',
    'Booking',
    'RestaurantProfile',
    'WaterSavingBadge',
    'UserWaterSavingHistory'
] 