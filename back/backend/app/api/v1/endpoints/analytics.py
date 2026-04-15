"""
Module: analytics.py
Layer: Endpoints
Description:
    Provides analytics overview endpoint.
Interacts with:
    - app.service.analytics_service
    - app.dependencies.auth
Called by:
    - API clients
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import require_role
from app.models.user import User, UserRole
from app.repository.analytics_repository import AnalyticsRepository
from app.schemas.analytics import AnalyticsOverview
from app.service.analytics_service import AnalyticsService

router = APIRouter()


@router.get('/overview', response_model=AnalyticsOverview)
async def overview(db: AsyncSession = Depends(get_db_session), current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.MANAGER))) -> AnalyticsOverview:
    return await AnalyticsService(AnalyticsRepository(db)).overview()
