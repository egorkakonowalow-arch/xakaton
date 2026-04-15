"""
Module: task_repository.py
Layer: Repository
Description:
    Performs task-related async DB operations.
Interacts with:
    - app.models.task
Called by:
    - app.service.task_service
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, task_id: int) -> Task | None:
        return await self.db.get(Task, task_id)

    async def list(self, offset: int, limit: int, assigned_to: int | None = None) -> tuple[list[Task], int]:
        stmt = select(Task)
        count_stmt = select(func.count()).select_from(Task)
        if assigned_to is not None:
            stmt = stmt.where(Task.assigned_to == assigned_to)
            count_stmt = count_stmt.where(Task.assigned_to == assigned_to)
        items = list((await self.db.scalars(stmt.offset(offset).limit(limit))).all())
        total = int(await self.db.scalar(count_stmt) or 0)
        return items, total

    async def create(self, task: Task) -> Task:
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update(self, task: Task) -> Task:
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()
