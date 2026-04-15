"""
Module: tasks.py
Layer: Endpoints
Description:
    Provides task CRUD and status update endpoints.
Interacts with:
    - app.service.task_service
Called by:
    - API clients
"""

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repository.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskStatusUpdate, TaskUpdate
from app.service.task_service import TaskService

router = APIRouter()


@router.get('', response_model=TaskListResponse)
async def list_tasks(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> TaskListResponse:
    items, total = await TaskService(TaskRepository(db)).list(page, size, current_user)
    return TaskListResponse(items=items, total=total, page=page, size=size)


@router.get('/{task_id}', response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await TaskService(TaskRepository(db)).get(task_id)


@router.post('', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await TaskService(TaskRepository(db)).create(payload, current_user)


@router.patch('/{task_id}', response_model=TaskResponse)
async def update_task(task_id: int, payload: TaskUpdate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await TaskService(TaskRepository(db)).update(task_id, payload, current_user)


@router.patch('/{task_id}/status', response_model=TaskResponse)
async def update_task_status(task_id: int, payload: TaskStatusUpdate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await TaskService(TaskRepository(db)).update(task_id, TaskUpdate(status=payload.status), current_user)
