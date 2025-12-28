from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class UserCreate(UserBase):
    phone: str


class OTPRequest(BaseModel):
    phone: str


class OTPVerify(BaseModel):
    phone: str
    code: str


class UserRead(UserBase):
    id: UUID
    is_active: bool
    is_admin: bool
    is_super_admin: bool
    is_support_agent: bool
    is_provisioning_specialist: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreateByAdmin(UserBase):
    phone: str
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_admin: bool = False
    is_super_admin: bool = False
    is_support_agent: bool = False
    is_provisioning_specialist: bool = False
    is_active: bool = True


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    is_admin: bool | None = None
    is_super_admin: bool | None = None
    is_support_agent: bool | None = None
    is_provisioning_specialist: bool | None = None
    is_active: bool | None = None


class UserActivateRequest(BaseModel):
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class TokenWithUser(Token):
    user: UserRead
