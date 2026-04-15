"""
Module: main.py
Layer: Application
Description:
    Creates FastAPI app, wires middleware/routers, and performs startup initialization.
Interacts with:
    - app.core.database
    - app.api.v1.router
Called by:
    - ASGI server
"""

from fastapi import FastAPI
from sqlalchemy import select

from app.api.v1.router import api_router
from app.core.database import AsyncSessionLocal, Base, engine
from app.core.security import get_password_hash
from app.middleware.logging import RequestLoggingMiddleware
from app.models import User
from app.models.user import UserRole

app = FastAPI(title="Hackathon Backend", version="1.0.0")
app.add_middleware(RequestLoggingMiddleware)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        admin = await session.scalar(select(User).where(User.email == "admin@local"))
        if not admin:
            session.add(User(full_name="System Administrator", email="admin@local", hashed_password=get_password_hash("admin123"), role=UserRole.ADMIN, is_active=True))
            await session.commit()
