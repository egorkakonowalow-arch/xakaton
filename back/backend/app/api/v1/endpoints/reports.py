"""
Module: reports.py
Layer: Endpoints
Description:
    Provides report CRUD, file upload, and export handlers.
Interacts with:
    - app.service.report_service
Called by:
    - API clients
"""

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repository.report_repository import ReportRepository
from app.schemas.report import ReportCreate, ReportListResponse, ReportResponse, ReportUpdate
from app.service.report_service import ReportService

router = APIRouter()


@router.get('', response_model=ReportListResponse)
async def list_reports(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> ReportListResponse:
    items, total = await ReportService(ReportRepository(db)).list(page, size)
    return ReportListResponse(items=items, total=total, page=page, size=size)


@router.get('/{report_id}', response_model=ReportResponse)
async def get_report(report_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await ReportService(ReportRepository(db)).get(report_id)


@router.post('', response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(payload: ReportCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await ReportService(ReportRepository(db)).create(payload, current_user)


@router.patch('/{report_id}', response_model=ReportResponse)
async def update_report(report_id: int, payload: ReportUpdate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return await ReportService(ReportRepository(db)).update(report_id, payload, current_user)


@router.post('/{report_id}/upload/{field_id}')
async def upload_file(report_id: int, field_id: int, upload: UploadFile = File(...), db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    path = await ReportService(ReportRepository(db)).upload_file(report_id, field_id, upload)
    return {'file_path': path}


@router.get('/{report_id}/export/pdf')
async def export_pdf(report_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> StreamingResponse:
    return StreamingResponse(iter([await ReportService(ReportRepository(db)).export_pdf(report_id)]), media_type='application/pdf')


@router.get('/{report_id}/export/excel')
async def export_excel(report_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)) -> StreamingResponse:
    return StreamingResponse(iter([await ReportService(ReportRepository(db)).export_excel_csv(report_id)]), media_type='text/csv')
