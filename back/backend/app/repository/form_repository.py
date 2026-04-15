"""
Module: form_repository.py
Layer: Repository
Description:
    Performs form template and field async DB operations.
Interacts with:
    - app.models.form
Called by:
    - app.service.form_service
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.form import FormField, FormTemplate


class FormRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_template_by_id(self, template_id: int) -> FormTemplate | None:
        return await self.db.get(FormTemplate, template_id)

    async def list_templates(self, offset: int, limit: int) -> tuple[list[FormTemplate], int]:
        items = list((await self.db.scalars(select(FormTemplate).offset(offset).limit(limit))).all())
        total = int(await self.db.scalar(select(func.count()).select_from(FormTemplate)) or 0)
        return items, total

    async def create_template(self, template: FormTemplate) -> FormTemplate:
        self.db.add(template)
        await self.db.commit()
        await self.db.refresh(template)
        return template

    async def update_template(self, template: FormTemplate) -> FormTemplate:
        await self.db.commit()
        await self.db.refresh(template)
        return template

    async def delete_template(self, template: FormTemplate) -> None:
        await self.db.delete(template)
        await self.db.commit()

    async def create_field(self, field: FormField) -> FormField:
        self.db.add(field)
        await self.db.commit()
        await self.db.refresh(field)
        return field
