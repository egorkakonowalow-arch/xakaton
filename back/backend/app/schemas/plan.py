"""
Module: plan.py
Layer: Schemas
Description:
    Defines plan and plan-item request/response schemas.
Interacts with:
    - app.service.plan_service
Called by:
    - plans endpoints
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.plan import PlanItemStatus, PlanStatus


class PlanItemCreate(BaseModel):
    title: str
    description: str | None = None
    target_count: int | None = None
    actual_count: int | None = None
    deadline: datetime | None = None
    status: PlanItemStatus = PlanItemStatus.PLANNED


class PlanItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    target_count: int | None = None
    actual_count: int | None = None
    deadline: datetime | None = None
    status: PlanItemStatus | None = None


class PlanItemResponse(PlanItemCreate):
    id: int
    plan_id: int

    model_config = ConfigDict(from_attributes=True)


class PlanCreate(BaseModel):
    title: str
    description: str | None = None
    district_id: int
    month: int
    year: int
    status: PlanStatus = PlanStatus.DRAFT


class PlanUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    district_id: int | None = None
    month: int | None = None
    year: int | None = None
    status: PlanStatus | None = None


class PlanResponse(PlanCreate):
    id: int
    created_by: int
    items: list[PlanItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


class PlanListResponse(BaseModel):
    items: list[PlanResponse]
    total: int
    page: int
    size: int
