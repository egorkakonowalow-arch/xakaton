"""
Module: users.py
Layer: Endpoints
Description:
    Provides thin user CRUD handlers.
Interacts with:
    - app.service.user_service
Called by:
    - API clients
"""

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.user import UserCreate, UserListResponse, UserResponse, UserUpdate
from app.service.user_service import UserService

router = APIRouter()


@router.get('', response_model=UserListResponse)
async def list_users(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> UserListResponse:
    items, total = await UserService(UserRepository(db)).list(page, size)
    return UserListResponse(items=items, total=total, page=page, size=size)


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> User:
    return await UserService(UserRepository(db)).get(user_id)


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> User:
    return await UserService(UserRepository(db)).create(payload, current_user)


@router.patch('/{user_id}', response_model=UserResponse)
async def update_user(user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> User:
    return await UserService(UserRepository(db)).update(user_id, payload, current_user)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> Response:
    await UserService(UserRepository(db)).delete(user_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
