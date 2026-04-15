"""
Module: __init__.py
Layer: Models
Description:
    Imports all ORM models to ensure metadata registration.
    Used by startup table creation in core/database.
Interacts with:
    - all model files in this package
Called by:
    - main.py during startup
"""

from app.models.district import District
from app.models.form import FormField, FormTemplate, FormValue
from app.models.notification import Notification
from app.models.plan import Plan, PlanItem
from app.models.report import Report
from app.models.task import Task
from app.models.user import User, UserDistrict

__all__ = [
    "District",
    "FormField",
    "FormTemplate",
    "FormValue",
    "Notification",
    "Plan",
    "PlanItem",
    "Report",
    "Task",
    "User",
    "UserDistrict",
]
