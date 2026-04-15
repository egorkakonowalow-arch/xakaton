"""
Module: districts.py
Layer: Endpoints
Description:
    Provides district CRUD and manager assignment endpoints.
Interacts with:
    - app.service.district_service
Called by:
    - API clients
"""

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repository.district_repository import DistrictRepository
from app.schemas.district import DistrictCreate, DistrictListResponse, DistrictResponse, DistrictUpdate, ManagerAssignmentRequest
from app.service.district_service import DistrictService

router = APIRouter()


@router.get('', response_model=DistrictListResponse)
async def list_districts(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> DistrictListResponse:
    items, total = await DistrictService(DistrictRepository(db)).list(page, size)
    return DistrictListResponse(items=items, total=total, page=page, size=size)


@router.get('/{district_id}', response_model=DistrictResponse)
async def get_district(district_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await DistrictService(DistrictRepository(db)).get(district_id)


@router.post('', response_model=DistrictResponse, status_code=status.HTTP_201_CREATED)
async def create_district(payload: DistrictCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await DistrictService(DistrictRepository(db)).create(payload, current_user)


@router.patch('/{district_id}', response_model=DistrictResponse)
async def update_district(district_id: int, payload: DistrictUpdate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await DistrictService(DistrictRepository(db)).update(district_id, payload, current_user)


@router.post('/{district_id}/assign-manager', status_code=status.HTTP_204_NO_CONTENT)
async def assign_manager(district_id: int, payload: ManagerAssignmentRequest, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> Response:
    await DistrictService(DistrictRepository(db)).repository.assign_manager(payload.user_id, district_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
