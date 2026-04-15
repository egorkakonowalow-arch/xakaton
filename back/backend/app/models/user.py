"""
Module: user.py
Layer: Models
Description:
    Defines user-related ORM entities, including users and manager-district mapping.
    Represents persistence structure only, without business logic.
    Provides relationship mappings for repository query composition.
Interacts with:
    - core/database.py (Base metadata)
    - models/district.py, models/task.py, models/report.py, models/notification.py
Called by:
    - repository/user_repository.py and other repositories
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserRole(str, Enum):
    """System roles for RBAC."""

    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class UserDistrict(Base):
    """Many-to-many relation between managers and districts."""

    __tablename__ = "user_districts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=False)


class User(Base):
    """Main user model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role"),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    district_id: Mapped[int | None] = mapped_column(ForeignKey("districts.id"), nullable=True)

    district = relationship("District", back_populates="users")
    managed_districts = relationship(
        "District",
        secondary="user_districts",
        back_populates="managers",
    )
    created_tasks = relationship(
        "Task",
        back_populates="creator",
        foreign_keys="Task.created_by",
    )
    assigned_tasks = relationship(
        "Task",
        back_populates="assignee",
        foreign_keys="Task.assigned_to",
    )
    plans = relationship("Plan", back_populates="creator")
    reports = relationship("Report", back_populates="submitter")
    notifications = relationship("Notification", back_populates="recipient")
