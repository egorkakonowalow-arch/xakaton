"""
Module: file_storage.py
Layer: Utils
Description:
    Stores uploaded files to uploads/{report_id}/{field_id}_{filename}.
Interacts with:
    - app.core.config
    - local filesystem
Called by:
    - app.service.report_service
"""

from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.core.config import settings


async def save_report_file(report_id: int, field_id: int, upload: UploadFile) -> Path:
    directory = Path(settings.UPLOAD_DIR) / str(report_id)
    directory.mkdir(parents=True, exist_ok=True)
    filename = (upload.filename or "file.bin").replace("/", "_").replace("\\", "_")
    target = directory / f"{field_id}_{filename}"
    async with aiofiles.open(target, "wb") as f:
        await f.write(await upload.read())
    return target
