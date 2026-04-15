"""
Module: database.py
Layer: Core
Description:
    Configures SQLAlchemy async engine, async session factory, and declarative base.
    Provides dependency helpers for database sessions.
    Contains infrastructure setup only.
Interacts with:
    - core/config.py
    - models/* via Base metadata
Called by:
    - repositories through injected AsyncSession
    - main.py startup initialization
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Base class for ORM models."""


engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yields async DB session for request lifecycle."""

    async with AsyncSessionLocal() as session:
        yield session
