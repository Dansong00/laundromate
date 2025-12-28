"""IoT Controller Pydantic schemas for Super-Admin Dashboard."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.core.models.iot_controller import ConnectivityStatus, DeviceType


class IoTControllerBase(BaseModel):
    """Base IoT controller schema with common fields."""

    mac_address: str
    serial_number: str | None = None
    machine_label: str
    device_type: DeviceType
    connectivity_status: ConnectivityStatus = ConnectivityStatus.UNKNOWN

    @field_validator("mac_address")
    @classmethod
    def validate_mac_address(cls, v: str) -> str:
        """Validate MAC address format."""
        import re

        pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        if not re.match(pattern, v):
            raise ValueError(
                "MAC address must be in format AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF"
            )
        return v

    @field_validator("machine_label")
    @classmethod
    def validate_machine_label(cls, v: str) -> str:
        """Validate machine label length."""
        if not v or len(v) > 100:
            raise ValueError("Machine label must be non-empty and max 100 characters")
        return v


class IoTControllerCreate(IoTControllerBase):
    """Schema for creating a new IoT controller."""

    store_id: UUID


class IoTControllerUpdate(BaseModel):
    """Schema for updating an IoT controller."""

    mac_address: str | None = None
    serial_number: str | None = None
    machine_label: str | None = None
    device_type: DeviceType | None = None
    connectivity_status: ConnectivityStatus | None = None
    last_heartbeat: datetime | None = None


class IoTControllerRead(IoTControllerBase):
    """Schema for reading an IoT controller."""

    id: UUID
    store_id: UUID
    last_heartbeat: datetime | None = None
    provisioned_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
