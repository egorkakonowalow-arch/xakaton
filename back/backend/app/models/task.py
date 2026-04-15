"""
Module: task.py
Layer: Models
Description:
    Defines task ORM model used for assignment and execution tracking.
    Contains status fields and references to users, district, and plan items.
    Holds database schema only.
Interacts with:
    - core/database.py
    - models/user.py, models/district.py, models/plan.py, models/notification.py
Called by:
    - repository/task_repository.py
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    OVERDUE = "overdue"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus, name="task_status"), default=TaskStatus.PENDING, nullable=False
    )
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    plan_item_id: Mapped[int | None] = mapped_column(ForeignKey("plan_items.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    creator = relationship("User", back_populates="created_tasks", foreign_keys=[created_by])
    assignee = relationship("User", back_populates="assigned_tasks", foreign_keys=[assigned_to])
    district = relationship("District", back_populates="tasks")
    plan_item = relationship("PlanItem", back_populates="tasks")
    notifications = relationship("Notification", back_populates="related_task")
