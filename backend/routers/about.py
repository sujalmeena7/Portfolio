from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException

from core.database import db
from core.security import require_admin
from models.schemas import About, AboutInput

router = APIRouter(prefix="/about", tags=["about"])


@router.get("", response_model=About)
async def get_about():
    doc = await db.about.find_one({}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "About not set yet")
    return doc


@router.put("", response_model=About)
async def upsert_about(body: AboutInput, _: dict = Depends(require_admin)):
    existing = await db.about.find_one({})
    payload = body.model_dump()
    payload["updated_at"] = datetime.now(timezone.utc)
    if existing:
        await db.about.update_one({"id": existing["id"]}, {"$set": payload})
        doc = await db.about.find_one({"id": existing["id"]}, {"_id": 0})
        return doc
    new = About(**body.model_dump()).model_dump()
    await db.about.insert_one(new)
    new.pop("_id", None)
    return new
