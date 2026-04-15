"""
Module: notification.py
Layer: Schemas
Description:
    Defines notification API schemas.
    Encapsulates request/response serialization for notification endpoints.
Interacts with:
    - service/notification_service.py
    - api/v1/endpoints/notifications.py
Called by:
    - FastAPI validation and response rendering
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    is_read: bool
    created_at: datetime
    related_task_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    page: int
    size: int
