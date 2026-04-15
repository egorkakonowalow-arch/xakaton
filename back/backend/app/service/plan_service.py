"""
Module: plan_service.py
Layer: Service
Description:
    Contains plan and plan-item business logic.
Interacts with:
    - app.repository.plan_repository
Called by:
    - plans endpoints
"""

from fastapi import HTTPException

from app.models.plan import Plan, PlanItem
from app.models.user import User, UserRole
from app.repository.plan_repository import PlanRepository
from app.schemas.plan import PlanCreate, PlanItemCreate, PlanItemUpdate, PlanUpdate


class PlanService:
    def __init__(self, repository: PlanRepository) -> None:
        self.repository = repository

    async def list(self, page: int, size: int) -> tuple[list[Plan], int]:
        return await self.repository.list_plans((page - 1) * size, size)

    async def get(self, plan_id: int) -> Plan:
        plan = await self.repository.get_plan_by_id(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return plan

    async def create(self, payload: PlanCreate, current_user: User) -> Plan:
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            raise HTTPException(status_code=403, detail="Forbidden")
        return await self.repository.create_plan(Plan(created_by=current_user.id, **payload.model_dump()))

    async def update(self, plan_id: int, payload: PlanUpdate, current_user: User) -> Plan:
        plan = await self.get(plan_id)
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            raise HTTPException(status_code=403, detail="Forbidden")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(plan, key, value)
        return await self.repository.update_plan(plan)

    async def delete(self, plan_id: int, current_user: User) -> None:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin")
        await self.repository.delete_plan(await self.get(plan_id))

    async def add_item(self, plan_id: int, payload: PlanItemCreate, current_user: User) -> PlanItem:
        await self.get(plan_id)
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            raise HTTPException(status_code=403, detail="Forbidden")
        return await self.repository.create_item(PlanItem(plan_id=plan_id, **payload.model_dump()))

    async def update_item(self, item_id: int, payload: PlanItemUpdate, current_user: User) -> PlanItem:
        item = await self.repository.get_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Plan item not found")
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            raise HTTPException(status_code=403, detail="Forbidden")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        return await self.repository.update_item(item)
