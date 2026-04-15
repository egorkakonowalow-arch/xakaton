"""
Module: notification_service.py
Layer: Service
Description:
    Contains notification ownership checks and read-state logic.
Interacts with:
    - app.repository.notification_repository
Called by:
    - notifications endpoints
"""

from fastapi import HTTPException

from app.models.notification import Notification
from app.models.user import User
from app.repository.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    async def list(self, user: User, page: int, size: int) -> tuple[list[Notification], int]:
        return await self.repository.list_for_user(user.id, (page - 1) * size, size)

    async def mark_read(self, notification_id: int, user: User) -> Notification:
        item = await self.repository.get_by_id(notification_id)
        if not item or item.user_id != user.id:
            raise HTTPException(status_code=404, detail="Notification not found")
        item.is_read = True
        return await self.repository.update(item)
