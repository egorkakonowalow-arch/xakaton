"""
Module: notification.py
Layer: Models
Description:
    Defines notification ORM model for system-generated user notifications.
    Stores read state and optional related task link.
    Contains persistence definitions only.
Interacts with:
    - core/database.py
    - models/user.py, models/task.py
Called by:
    - repository/notification_repository.py
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    related_task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"), nullable=True)

    recipient = relationship("User", back_populates="notifications")
    related_task = relationship("Task", back_populates="notifications")
