"""
Module: report_service.py
Layer: Service
Description:
    Contains report workflow logic, exports, and file uploads.
Interacts with:
    - app.repository.report_repository
    - app.utils.export
    - app.utils.file_storage
Called by:
    - reports endpoints
"""

from fastapi import HTTPException, UploadFile

from app.models.form import FormValue
from app.models.report import Report, ReportStatus
from app.models.user import User, UserRole
from app.repository.report_repository import ReportRepository
from app.schemas.report import ReportCreate, ReportUpdate
from app.utils.export import build_report_csv_bytes, build_report_pdf_bytes
from app.utils.file_storage import save_report_file


class ReportService:
    def __init__(self, repository: ReportRepository) -> None:
        self.repository = repository

    async def list(self, page: int, size: int) -> tuple[list[Report], int]:
        return await self.repository.list((page - 1) * size, size)

    async def get(self, report_id: int) -> Report:
        report = await self.repository.get_by_id(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report

    async def create(self, payload: ReportCreate, current_user: User) -> Report:
        report = await self.repository.create(Report(template_id=payload.template_id, submitted_by=current_user.id, district_id=payload.district_id, plan_item_id=payload.plan_item_id, status=ReportStatus.SUBMITTED))
        for value in payload.values:
            await self.repository.add_value(FormValue(report_id=report.id, field_id=value.field_id, value_text=value.value_text, value_number=value.value_number, file_path=value.file_path))
        return await self.get(report.id)

    async def update(self, report_id: int, payload: ReportUpdate, current_user: User) -> Report:
        report = await self.get(report_id)
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER} and report.submitted_by != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(report, key, value)
        return await self.repository.update(report)

    async def upload_file(self, report_id: int, field_id: int, upload: UploadFile) -> str:
        await self.get(report_id)
        return str(await save_report_file(report_id, field_id, upload))

    async def export_pdf(self, report_id: int) -> bytes:
        return build_report_pdf_bytes(await self.get(report_id))

    async def export_excel_csv(self, report_id: int) -> bytes:
        return build_report_csv_bytes(await self.get(report_id))
