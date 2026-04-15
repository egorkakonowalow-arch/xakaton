"""
Module: task.py
Layer: Schemas
Description:
    Defines request and response schemas for task management operations.
    Enforces payload structure and paginated list response contract.
Interacts with:
    - service/task_service.py
    - api/v1/endpoints/tasks.py
Called by:
    - FastAPI validation pipeline
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    assigned_to: int
    district_id: int
    deadline: datetime | None = None
    plan_item_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assigned_to: int | None = None
    district_id: int | None = None
    deadline: datetime | None = None
    status: TaskStatus | None = None
    completed_at: datetime | None = None
    plan_item_id: int | None = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    created_by: int
    assigned_to: int
    district_id: int
    status: TaskStatus
    deadline: datetime | None
    completed_at: datetime | None
    plan_item_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    size: int
