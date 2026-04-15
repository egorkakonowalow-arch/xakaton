"""
Module: report_repository.py
Layer: Repository
Description:
    Performs report and report-value async DB operations.
Interacts with:
    - app.models.report
    - app.models.form
Called by:
    - app.service.report_service
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.form import FormValue
from app.models.report import Report


class ReportRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, report_id: int) -> Report | None:
        return await self.db.get(Report, report_id)

    async def list(self, offset: int, limit: int) -> tuple[list[Report], int]:
        items = list((await self.db.scalars(select(Report).offset(offset).limit(limit))).all())
        total = int(await self.db.scalar(select(func.count()).select_from(Report)) or 0)
        return items, total

    async def create(self, report: Report) -> Report:
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        return report

    async def update(self, report: Report) -> Report:
        await self.db.commit()
        await self.db.refresh(report)
        return report

    async def add_value(self, value: FormValue) -> FormValue:
        self.db.add(value)
        await self.db.commit()
        await self.db.refresh(value)
        return value
