"""
Module: analytics.py
Layer: Schemas
Description:
    Defines analytics response DTOs.
Interacts with:
    - app.service.analytics_service
Called by:
    - analytics endpoints
"""

from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    tasks_total: int
    reports_total: int
    plans_total: int
