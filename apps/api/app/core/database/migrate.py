from app.core.models import Base
from app.core.database.session import engine

# Import all models to register them with SQLAlchemy's Base metadata
from app.core.models.user import User  # noqa: F401
from app.core.models.customer import Customer  # noqa: F401
from app.core.models.address import Address  # noqa: F401
from app.core.models.service import Service  # noqa: F401
from app.core.models.order import Order, OrderStatus  # noqa: F401
from app.core.models.order_item import OrderItem  # noqa: F401
from app.core.models.notification import Notification, NotificationType, NotificationStatus  # noqa: F401


def create_all_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_all_tables()
