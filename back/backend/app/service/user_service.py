"""
Module: user_service.py
Layer: Service
Description:
    Contains user business logic and auth token issuance.
Interacts with:
    - app.repository.user_repository
    - app.core.security
Called by:
    - auth and users endpoints
"""

from datetime import timedelta

from fastapi import HTTPException

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User, UserRole
from app.repository.user_repository import UserRepository
from app.schemas.user import LoginRequest, UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def login(self, payload: LoginRequest) -> str:
        user = await self.repository.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return create_access_token(str(user.id), timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    async def list(self, page: int, size: int) -> tuple[list[User], int]:
        return await self.repository.list((page - 1) * size, size)

    async def get(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create(self, payload: UserCreate, current_user: User) -> User:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin can create users")
        if await self.repository.get_by_email(payload.email):
            raise HTTPException(status_code=400, detail="Email already exists")
        user = User(full_name=payload.full_name, email=payload.email, role=payload.role, district_id=payload.district_id, hashed_password=get_password_hash(payload.password), is_active=True)
        return await self.repository.create(user)

    async def update(self, user_id: int, payload: UserUpdate, current_user: User) -> User:
        user = await self.get(user_id)
        if current_user.role != UserRole.ADMIN and current_user.id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")
        data = payload.model_dump(exclude_unset=True)
        if "password" in data:
            user.hashed_password = get_password_hash(data.pop("password"))
        for key, value in data.items():
            setattr(user, key, value)
        return await self.repository.update(user)

    async def delete(self, user_id: int, current_user: User) -> None:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin can delete users")
        user = await self.get(user_id)
        await self.repository.delete(user)
