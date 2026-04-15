"""
Module: district.py
Layer: Models
Description:
    Defines district ORM entity.
    Maps district relations to users, tasks, plans, and reports.
    Contains schema metadata only.
Interacts with:
    - core/database.py
    - models/user.py and related domain models
Called by:
    - repository/district_repository.py
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class District(Base):
    """Municipal district model."""

    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    users = relationship("User", back_populates="district")
    managers = relationship("User", secondary="user_districts", back_populates="managed_districts")
    tasks = relationship("Task", back_populates="district")
    plans = relationship("Plan", back_populates="district")
    reports = relationship("Report", back_populates="district")
