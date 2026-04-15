"""
Module: form.py
Layer: Schemas
Description:
    Defines form template and field schemas.
Interacts with:
    - app.service.form_service
Called by:
    - forms endpoints
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.form import FormFieldType


class FormFieldCreate(BaseModel):
    label: str
    field_type: FormFieldType
    is_required: bool = True
    order: int
    options: list[Any] | None = None


class FormFieldResponse(FormFieldCreate):
    id: int
    template_id: int

    model_config = ConfigDict(from_attributes=True)


class FormTemplateCreate(BaseModel):
    title: str
    description: str | None = None
    fields: list[FormFieldCreate] = []


class FormTemplateUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class FormTemplateResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    created_by: int
    created_at: datetime
    fields: list[FormFieldResponse] = []

    model_config = ConfigDict(from_attributes=True)


class FormTemplateListResponse(BaseModel):
    items: list[FormTemplateResponse]
    total: int
    page: int
    size: int
