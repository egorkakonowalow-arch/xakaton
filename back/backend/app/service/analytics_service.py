"""
Module: analytics_service.py
Layer: Service
Description:
    Builds analytics overview DTO from repository aggregates.
Interacts with:
    - app.repository.analytics_repository
Called by:
    - analytics endpoints
"""

from app.repository.analytics_repository import AnalyticsRepository
from app.schemas.analytics import AnalyticsOverview


class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository) -> None:
        self.repository = repository

    async def overview(self) -> AnalyticsOverview:
        return AnalyticsOverview(tasks_total=await self.repository.task_count(), reports_total=await self.repository.report_count(), plans_total=await self.repository.plan_count())
