"""
Module: notification_repository.py
Layer: Repository
Description:
    Performs notification async DB operations.
Interacts with:
    - app.models.notification
Called by:
    - app.service.notification_service
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification


class NotificationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_for_user(self, user_id: int, offset: int, limit: int) -> tuple[list[Notification], int]:
        stmt = select(Notification).where(Notification.user_id == user_id)
        items = list((await self.db.scalars(stmt.offset(offset).limit(limit))).all())
        total = int(await self.db.scalar(select(func.count()).select_from(Notification).where(Notification.user_id == user_id)) or 0)
        return items, total

    async def get_by_id(self, notification_id: int) -> Notification | None:
        return await self.db.get(Notification, notification_id)

    async def update(self, notification: Notification) -> Notification:
        await self.db.commit()
        await self.db.refresh(notification)
        return notification
