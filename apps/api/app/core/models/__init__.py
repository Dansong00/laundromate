from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .customer import Customer
from .address import Address
from .service import Service
from .order import Order, OrderStatus
from .order_item import OrderItem
from .notification import Notification, NotificationType, NotificationStatus
