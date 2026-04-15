"""
Module: notifications.py
Layer: Endpoints
Description:
    Provides notification list and read endpoints.
Interacts with:
    - app.service.notification_service
Called by:
    - API clients
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repository.notification_repository import NotificationRepository
from app.schemas.notification import NotificationListResponse, NotificationResponse
from app.service.notification_service import NotificationService

router = APIRouter()


@router.get('', response_model=NotificationListResponse)
async def list_notifications(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> NotificationListResponse:
    items, total = await NotificationService(NotificationRepository(db)).list(current_user, page, size)
    return NotificationListResponse(items=items, total=total, page=page, size=size)


@router.patch('/{notification_id}/read', response_model=NotificationResponse)
async def mark_read(notification_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await NotificationService(NotificationRepository(db)).mark_read(notification_id, current_user)
