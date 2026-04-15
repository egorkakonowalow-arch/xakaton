"""
Module: logging.py
Layer: Middleware
Description:
    Logs request method, path, status, and latency.
Interacts with:
    - Python logging
Called by:
    - FastAPI middleware stack
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("backend.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        start = time.perf_counter()
        response = await call_next(request)
        logger.info("%s %s -> %s (%.2fms)", request.method, request.url.path, response.status_code, (time.perf_counter() - start) * 1000)
        return response
