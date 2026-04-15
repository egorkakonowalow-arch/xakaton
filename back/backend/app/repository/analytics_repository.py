"""
Module: analytics_repository.py
Layer: Repository
Description:
    Provides aggregate count queries for analytics.
Interacts with:
    - app.models.task
    - app.models.report
    - app.models.plan
Called by:
    - app.service.analytics_service
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan import Plan
from app.models.report import Report
from app.models.task import Task


class AnalyticsRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def task_count(self) -> int:
        return int(await self.db.scalar(select(func.count()).select_from(Task)) or 0)

    async def report_count(self) -> int:
        return int(await self.db.scalar(select(func.count()).select_from(Report)) or 0)

    async def plan_count(self) -> int:
        return int(await self.db.scalar(select(func.count()).select_from(Plan)) or 0)
