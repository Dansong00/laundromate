"""User-Store association model for many-to-many relationship."""

import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.models import Base


class UserStoreRole(str, enum.Enum):
    """User-Store role enum."""

    OWNER = "owner"
    OPERATOR = "operator"


class UserStore(Base):
    """User-Store association model for many-to-many relationship."""

    __tablename__ = "user_stores"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    store_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = Column(Enum(UserStoreRole), nullable=False, default=UserStoreRole.OWNER)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user = relationship("User")
    store = relationship("Store", back_populates="user_stores")

    # Constraints
    __table_args__ = (
        Index("ix_user_stores_user_store", "user_id", "store_id", unique=True),
    )
