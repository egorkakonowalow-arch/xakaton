"""
Module: report.py
Layer: Schemas
Description:
    Defines report submission and response schemas.
Interacts with:
    - app.service.report_service
Called by:
    - reports endpoints
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.report import ReportStatus


class ReportValueCreate(BaseModel):
    field_id: int
    value_text: str | None = None
    value_number: float | None = None
    file_path: str | None = None


class ReportValueResponse(ReportValueCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReportCreate(BaseModel):
    template_id: int
    district_id: int
    plan_item_id: int | None = None
    values: list[ReportValueCreate] = []


class ReportUpdate(BaseModel):
    status: ReportStatus | None = None


class ReportResponse(BaseModel):
    id: int
    template_id: int
    submitted_by: int
    district_id: int
    plan_item_id: int | None = None
    submitted_at: datetime
    status: ReportStatus
    values: list[ReportValueResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ReportListResponse(BaseModel):
    items: list[ReportResponse]
    total: int
    page: int
    size: int
