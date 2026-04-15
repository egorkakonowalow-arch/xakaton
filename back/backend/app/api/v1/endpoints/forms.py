"""
Module: forms.py
Layer: Endpoints
Description:
    Provides form template endpoints.
Interacts with:
    - app.service.form_service
Called by:
    - API clients
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repository.form_repository import FormRepository
from app.schemas.form import FormFieldCreate, FormFieldResponse, FormTemplateCreate, FormTemplateListResponse, FormTemplateResponse, FormTemplateUpdate
from app.service.form_service import FormService

router = APIRouter()


@router.get('', response_model=FormTemplateListResponse)
async def list_templates(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> FormTemplateListResponse:
    items, total = await FormService(FormRepository(db)).list(page, size)
    return FormTemplateListResponse(items=items, total=total, page=page, size=size)


@router.get('/{template_id}', response_model=FormTemplateResponse)
async def get_template(template_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await FormService(FormRepository(db)).get(template_id)


@router.post('', response_model=FormTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(payload: FormTemplateCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await FormService(FormRepository(db)).create(payload, current_user)


@router.post('/{template_id}/fields', response_model=FormFieldResponse, status_code=status.HTTP_201_CREATED)
async def add_field(template_id: int, payload: FormFieldCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await FormService(FormRepository(db)).add_field(template_id, payload, current_user)
