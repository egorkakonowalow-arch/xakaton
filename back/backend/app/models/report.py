"""
Module: report.py
Layer: Models
Description:
    Defines submitted report ORM model with review lifecycle status.
    Connects submitted report instances to templates, users, districts, and plan items.
    Contains only declarative persistence structure.
Interacts with:
    - core/database.py
    - models/form.py, models/user.py, models/district.py, models/plan.py
Called by:
    - repository/report_repository.py
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReportStatus(str, Enum):
    SUBMITTED = "submitted"
    REVIEWED = "reviewed"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("form_templates.id"), nullable=False)
    submitted_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=False)
    plan_item_id: Mapped[int | None] = mapped_column(ForeignKey("plan_items.id"), nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[ReportStatus] = mapped_column(
        SQLEnum(ReportStatus, name="report_status"), default=ReportStatus.SUBMITTED, nullable=False
    )

    template = relationship("FormTemplate", back_populates="reports")
    submitter = relationship("User", back_populates="reports")
    district = relationship("District", back_populates="reports")
    plan_item = relationship("PlanItem", back_populates="reports")
    values = relationship("FormValue", back_populates="report", cascade="all, delete-orphan")
