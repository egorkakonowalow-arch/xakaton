"""
Module: auth.py
Layer: Endpoints
Description:
    Exposes login and current user endpoints.
Interacts with:
    - app.service.user_service
    - app.dependencies.auth
Called by:
    - API clients
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.user import LoginRequest, TokenResponse, UserResponse
from app.service.user_service import UserService

router = APIRouter()


@router.post('/login', response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db_session)) -> TokenResponse:
    return TokenResponse(access_token=await UserService(UserRepository(db)).login(payload))


@router.get('/me', response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
