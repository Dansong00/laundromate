from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Import all models to ensure they are registered with SQLAlchemy
from app.core.models.address import Address  # noqa: E402
from app.core.models.agent_configuration import AgentConfiguration  # noqa: E402
from app.core.models.ai_agent import AgentCategory, AIAgent  # noqa: E402
from app.core.models.customer import Customer  # noqa: E402
from app.core.models.invitation import Invitation, InvitationStatus  # noqa: E402
from app.core.models.iot_controller import (  # noqa: E402
    ConnectivityStatus,
    DeviceType,
    IoTController,
)
from app.core.models.notification import Notification  # noqa: E402
from app.core.models.order import Order  # noqa: E402
from app.core.models.order_item import OrderItem  # noqa: E402

# Super-Admin Dashboard models
from app.core.models.organization import Organization, OrganizationStatus  # noqa: E402
from app.core.models.service import Service  # noqa: E402
from app.core.models.store import Store, StoreStatus  # noqa: E402
from app.core.models.user import User  # noqa: E402
from app.core.models.user_store import UserStore, UserStoreRole  # noqa: E402
from app.core.models.verification_code import VerificationCode  # noqa: E402

__all__ = [
    "Base",
    "Address",
    "Customer",
    "Notification",
    "Order",
    "OrderItem",
    "Service",
    "User",
    "VerificationCode",
    "Organization",
    "OrganizationStatus",
    "Store",
    "StoreStatus",
    "IoTController",
    "DeviceType",
    "ConnectivityStatus",
    "AgentConfiguration",
    "AIAgent",
    "AgentCategory",
    "Invitation",
    "InvitationStatus",
    "UserStore",
    "UserStoreRole",
]
