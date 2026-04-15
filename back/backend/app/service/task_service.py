"""
Module: task_service.py
Layer: Service
Description:
    Contains task business rules and status transitions.
Interacts with:
    - app.repository.task_repository
Called by:
    - tasks endpoints
"""

from datetime import UTC, datetime

from fastapi import HTTPException

from app.models.task import Task, TaskStatus
from app.models.user import User, UserRole
from app.repository.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    async def list(self, page: int, size: int, current_user: User) -> tuple[list[Task], int]:
        assigned = current_user.id if current_user.role == UserRole.EMPLOYEE else None
        return await self.repository.list((page - 1) * size, size, assigned)

    async def get(self, task_id: int) -> Task:
        task = await self.repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def create(self, payload: TaskCreate, current_user: User) -> Task:
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            raise HTTPException(status_code=403, detail="Forbidden")
        task = Task(title=payload.title, description=payload.description, created_by=current_user.id, assigned_to=payload.assigned_to, district_id=payload.district_id, deadline=payload.deadline, plan_item_id=payload.plan_item_id)
        return await self.repository.create(task)

    async def update(self, task_id: int, payload: TaskUpdate, current_user: User) -> Task:
        task = await self.get(task_id)
        if current_user.role == UserRole.EMPLOYEE and task.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        if task.status == TaskStatus.DONE and not task.completed_at:
            task.completed_at = datetime.now(UTC)
        return await self.repository.update(task)

    async def delete(self, task_id: int, current_user: User) -> None:
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            raise HTTPException(status_code=403, detail="Forbidden")
        await self.repository.delete(await self.get(task_id))
