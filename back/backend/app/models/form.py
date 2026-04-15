"""
Module: form.py
Layer: Models
Description:
    Defines report form templates, fields, and submitted values ORM entities.
    Encapsulates persistence shape for dynamic form subsystem.
    Contains no service-level validation rules.
Interacts with:
    - core/database.py
    - models/report.py, models/user.py
Called by:
    - repository/form_repository.py and repository/report_repository.py
"""

from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FormFieldType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    FILE = "file"
    DATE = "date"
    SELECT = "select"


class FormTemplate(Base):
    __tablename__ = "form_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    fields = relationship("FormField", back_populates="template", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="template")


class FormField(Base):
    __tablename__ = "form_fields"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("form_templates.id"), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    field_type: Mapped[FormFieldType] = mapped_column(
        SQLEnum(FormFieldType, name="form_field_type"), nullable=False
    )
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    options: Mapped[list[Any] | None] = mapped_column(JSON, nullable=True)

    template = relationship("FormTemplate", back_populates="fields")
    values = relationship("FormValue", back_populates="field")


class FormValue(Base):
    __tablename__ = "form_values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), nullable=False)
    field_id: Mapped[int] = mapped_column(ForeignKey("form_fields.id"), nullable=False)
    value_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    value_number: Mapped[float | None] = mapped_column(Float, nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    report = relationship("Report", back_populates="values")
    field = relationship("FormField", back_populates="values")
