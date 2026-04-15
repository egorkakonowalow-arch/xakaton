"""
Module: user_repository.py
Layer: Repository
Description:
    Performs async SQLAlchemy operations for users.
Interacts with:
    - app.models.user
Called by:
    - app.service.user_service
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.db.scalar(select(User).where(User.email == email))

    async def list(self, offset: int, limit: int) -> tuple[list[User], int]:
        items = list((await self.db.scalars(select(User).offset(offset).limit(limit))).all())
        total = int(await self.db.scalar(select(func.count()).select_from(User)) or 0)
        return items, total

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()
