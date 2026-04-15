"""
Module: district_repository.py
Layer: Repository
Description:
    Performs district DB operations and manager mapping writes.
Interacts with:
    - app.models.district
    - app.models.user
Called by:
    - app.service.district_service
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.district import District
from app.models.user import UserDistrict


class DistrictRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, district_id: int) -> District | None:
        return await self.db.get(District, district_id)

    async def get_by_code(self, code: str) -> District | None:
        return await self.db.scalar(select(District).where(District.code == code))

    async def list(self, offset: int, limit: int) -> tuple[list[District], int]:
        items = list((await self.db.scalars(select(District).offset(offset).limit(limit))).all())
        total = int(await self.db.scalar(select(func.count()).select_from(District)) or 0)
        return items, total

    async def create(self, district: District) -> District:
        self.db.add(district)
        await self.db.commit()
        await self.db.refresh(district)
        return district

    async def update(self, district: District) -> District:
        await self.db.commit()
        await self.db.refresh(district)
        return district

    async def delete(self, district: District) -> None:
        await self.db.delete(district)
        await self.db.commit()

    async def assign_manager(self, user_id: int, district_id: int) -> UserDistrict:
        mapping = UserDistrict(user_id=user_id, district_id=district_id)
        self.db.add(mapping)
        await self.db.commit()
        await self.db.refresh(mapping)
        return mapping
