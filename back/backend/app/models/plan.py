"""
Module: plan.py
Layer: Models
Description:
    Defines monthly plan and plan item ORM entities.
    Stores planning state and KPI fields for execution tracking.
    Contains persistence mappings only.
Interacts with:
    - core/database.py
    - models/user.py, models/district.py, models/task.py, models/report.py
Called by:
    - repository/plan_repository.py
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PlanStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"


class PlanItemStatus(str, Enum):
    PLANNED = "planned"
    DONE = "done"


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[PlanStatus] = mapped_column(
        SQLEnum(PlanStatus, name="plan_status"), default=PlanStatus.DRAFT, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    creator = relationship("User", back_populates="plans")
    district = relationship("District", back_populates="plans")
    items = relationship("PlanItem", back_populates="plan", cascade="all, delete-orphan")


class PlanItem(Base):
    __tablename__ = "plan_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actual_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[PlanItemStatus] = mapped_column(
        SQLEnum(PlanItemStatus, name="plan_item_status"),
        default=PlanItemStatus.PLANNED,
        nullable=False,
    )

    plan = relationship("Plan", back_populates="items")
    tasks = relationship("Task", back_populates="plan_item")
    reports = relationship("Report", back_populates="plan_item")
