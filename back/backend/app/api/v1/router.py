"""
Module: router.py
Layer: API v1
Description:
    Aggregates all v1 endpoint routers.
Interacts with:
    - app.api.v1.endpoints.*
Called by:
    - main.py
"""

from fastapi import APIRouter

from app.api.v1.endpoints import analytics, auth, districts, forms, notifications, plans, reports, tasks, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(districts.router, prefix="/districts", tags=["districts"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(plans.router, prefix="/plans", tags=["plans"])
api_router.include_router(forms.router, prefix="/forms", tags=["forms"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
