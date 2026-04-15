"""
Module: plan_repository.py
Layer: Repository
Description:
    Performs plan and plan-item async DB operations.
Interacts with:
    - app.models.plan
Called by:
    - app.service.plan_service
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan import Plan, PlanItem


class PlanRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_plan_by_id(self, plan_id: int) -> Plan | None:
        return await self.db.get(Plan, plan_id)

    async def list_plans(self, offset: int, limit: int) -> tuple[list[Plan], int]:
        items = list((await self.db.scalars(select(Plan).offset(offset).limit(limit))).all())
        total = int(await self.db.scalar(select(func.count()).select_from(Plan)) or 0)
        return items, total

    async def create_plan(self, plan: Plan) -> Plan:
        self.db.add(plan)
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def update_plan(self, plan: Plan) -> Plan:
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def delete_plan(self, plan: Plan) -> None:
        await self.db.delete(plan)
        await self.db.commit()

    async def get_item_by_id(self, item_id: int) -> PlanItem | None:
        return await self.db.get(PlanItem, item_id)

    async def create_item(self, item: PlanItem) -> PlanItem:
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_item(self, item: PlanItem) -> PlanItem:
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete_item(self, item: PlanItem) -> None:
        await self.db.delete(item)
        await self.db.commit()
