"""
Module: plans.py
Layer: Endpoints
Description:
    Provides plan and plan-item endpoints.
Interacts with:
    - app.service.plan_service
Called by:
    - API clients
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repository.plan_repository import PlanRepository
from app.schemas.plan import PlanCreate, PlanItemCreate, PlanItemResponse, PlanItemUpdate, PlanListResponse, PlanResponse, PlanUpdate
from app.service.plan_service import PlanService

router = APIRouter()


@router.get('', response_model=PlanListResponse)
async def list_plans(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> PlanListResponse:
    items, total = await PlanService(PlanRepository(db)).list(page, size)
    return PlanListResponse(items=items, total=total, page=page, size=size)


@router.get('/{plan_id}', response_model=PlanResponse)
async def get_plan(plan_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await PlanService(PlanRepository(db)).get(plan_id)


@router.post('', response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
async def create_plan(payload: PlanCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await PlanService(PlanRepository(db)).create(payload, current_user)


@router.post('/{plan_id}/items', response_model=PlanItemResponse, status_code=status.HTTP_201_CREATED)
async def add_item(plan_id: int, payload: PlanItemCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await PlanService(PlanRepository(db)).add_item(plan_id, payload, current_user)


@router.patch('/items/{item_id}', response_model=PlanItemResponse)
async def update_item(item_id: int, payload: PlanItemUpdate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await PlanService(PlanRepository(db)).update_item(item_id, payload, current_user)
