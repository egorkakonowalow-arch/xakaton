"""
Module: district_service.py
Layer: Service
Description:
    Contains district business rules and permission checks.
Interacts with:
    - app.repository.district_repository
Called by:
    - districts endpoints
"""

from fastapi import HTTPException

from app.models.district import District
from app.models.user import User, UserRole
from app.repository.district_repository import DistrictRepository
from app.schemas.district import DistrictCreate, DistrictUpdate


class DistrictService:
    def __init__(self, repository: DistrictRepository) -> None:
        self.repository = repository

    async def list(self, page: int, size: int) -> tuple[list[District], int]:
        return await self.repository.list((page - 1) * size, size)

    async def get(self, district_id: int) -> District:
        district = await self.repository.get_by_id(district_id)
        if not district:
            raise HTTPException(status_code=404, detail="District not found")
        return district

    async def create(self, payload: DistrictCreate, current_user: User) -> District:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin")
        district = District(name=payload.name, code=payload.code)
        return await self.repository.create(district)

    async def update(self, district_id: int, payload: DistrictUpdate, current_user: User) -> District:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin")
        district = await self.get(district_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(district, key, value)
        return await self.repository.update(district)

    async def delete(self, district_id: int, current_user: User) -> None:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin")
        await self.repository.delete(await self.get(district_id))
