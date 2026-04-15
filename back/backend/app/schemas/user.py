"""
Module: user.py
Layer: Schemas
Description:
    Defines request and response Pydantic schemas for user and auth operations.
    Controls API data contracts without business logic.
Interacts with:
    - api/v1/endpoints/users.py
    - service/user_service.py
Called by:
    - FastAPI request and response validation
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: UserRole
    district_id: int | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: UserRole | None = None
    district_id: int | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    size: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
