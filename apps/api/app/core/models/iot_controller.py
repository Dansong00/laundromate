"""IoT Controller model for Super-User Admin Dashboard."""

import enum
import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text

from app.core.models import Base


class DeviceType(str, enum.Enum):
    """Device type enum."""

    WASHER = "washer"
    DRYER = "dryer"
    OTHER = "other"


class ConnectivityStatus(str, enum.Enum):
    """Connectivity status enum."""

    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


class IoTController(Base):
    """IoT Controller model representing a physical hardware device."""

    __tablename__ = "iot_controllers"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    mac_address = Column(String(17), nullable=False)  # Format: AA:BB:CC:DD:EE:FF
    serial_number = Column(String(100), nullable=True)
    machine_label = Column(String(100), nullable=False)
    device_type = Column(Enum(DeviceType), nullable=False)
    connectivity_status = Column(
        Enum(ConnectivityStatus),
        nullable=False,
        default=ConnectivityStatus.UNKNOWN,
    )
    last_heartbeat = Column(DateTime(timezone=True), nullable=True)
    provisioned_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    store = relationship("Store", back_populates="iot_controllers")

    # Constraints
    __table_args__ = (
        UniqueConstraint("store_id", "mac_address", name="uq_iot_store_mac"),
        Index(
            "ix_iot_store_serial",
            "store_id",
            "serial_number",
            unique=True,
            postgresql_where=text("serial_number IS NOT NULL"),
        ),
    )
