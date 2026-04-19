import os
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from core.config import settings
from core.security import require_admin

router = APIRouter(prefix="/uploads", tags=["uploads"])

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".pdf"}
MAX_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post("")
async def upload_file(file: UploadFile = File(...), _: dict = Depends(require_admin)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, f"Unsupported file type: {ext}")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "File too large (max 10MB)")

    safe_name = f"{uuid.uuid4().hex}{ext}"
    path = Path(settings.UPLOAD_DIR) / safe_name
    path.write_bytes(data)

    return {
        "filename": safe_name,
        "url": f"{settings.PUBLIC_UPLOAD_BASE}/{safe_name}",
        "size": len(data),
        "content_type": file.content_type,
    }


@router.get("/{filename}")
async def serve_file(filename: str):
    # Prevent path traversal
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise HTTPException(400, "Invalid filename")
    path = Path(settings.UPLOAD_DIR) / filename
    if not path.exists() or not path.is_file():
        raise HTTPException(404, "Not found")
    return FileResponse(str(path))
