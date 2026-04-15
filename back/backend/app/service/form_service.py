"""
Module: form_service.py
Layer: Service
Description:
    Contains form template business logic.
Interacts with:
    - app.repository.form_repository
Called by:
    - forms endpoints
"""

from fastapi import HTTPException

from app.models.form import FormField, FormTemplate
from app.models.user import User, UserRole
from app.repository.form_repository import FormRepository
from app.schemas.form import FormFieldCreate, FormTemplateCreate, FormTemplateUpdate


class FormService:
    def __init__(self, repository: FormRepository) -> None:
        self.repository = repository

    async def list(self, page: int, size: int) -> tuple[list[FormTemplate], int]:
        return await self.repository.list_templates((page - 1) * size, size)

    async def get(self, template_id: int) -> FormTemplate:
        template = await self.repository.get_template_by_id(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        return template

    async def create(self, payload: FormTemplateCreate, current_user: User) -> FormTemplate:
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            raise HTTPException(status_code=403, detail="Forbidden")
        template = await self.repository.create_template(FormTemplate(title=payload.title, description=payload.description, created_by=current_user.id))
        for field in payload.fields:
            await self.repository.create_field(FormField(template_id=template.id, **field.model_dump()))
        return await self.get(template.id)

    async def update(self, template_id: int, payload: FormTemplateUpdate, current_user: User) -> FormTemplate:
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            raise HTTPException(status_code=403, detail="Forbidden")
        template = await self.get(template_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(template, key, value)
        return await self.repository.update_template(template)

    async def add_field(self, template_id: int, payload: FormFieldCreate, current_user: User) -> FormField:
        await self.get(template_id)
        if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            raise HTTPException(status_code=403, detail="Forbidden")
        return await self.repository.create_field(FormField(template_id=template_id, **payload.model_dump()))
