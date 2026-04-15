"""
Module: district.py
Layer: Schemas
Description:
    Defines Pydantic schemas for district API payloads and paginated results.
    Keeps serialization contracts separate from service and repository logic.
Interacts with:
    - service/district_service.py
    - api/v1/endpoints/districts.py
Called by:
    - FastAPI schema validation
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DistrictCreate(BaseModel):
    name: str
    code: str


class DistrictUpdate(BaseModel):
    name: str | None = None
    code: str | None = None


class DistrictResponse(BaseModel):
    id: int
    name: str
    code: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DistrictListResponse(BaseModel):
    items: list[DistrictResponse]
    total: int
    page: int
    size: int


class ManagerAssignmentRequest(BaseModel):
    user_id: int
