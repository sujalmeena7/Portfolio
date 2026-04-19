from datetime import datetime, timezone
from fastapi import APIRouter, Depends

from core.database import db
from core.security import require_admin
from models.schemas import About, AboutInput

router = APIRouter(prefix="/about", tags=["about"])


def _default_about() -> dict:
    return About(
        name="Alex Vantage",
        role="Creative Full-Stack Developer",
        tagline="Designing and shipping high-impact digital products.",
        bio=[
            "I build performant web apps with clean architecture and strong UX.",
            "I specialize in React + FastAPI systems with production-ready delivery.",
        ],
        location="Remote",
        email="hello@alexvantage.dev",
        available=True,
        stats=[],
        socials={},
    ).model_dump()


@router.get("", response_model=About)
@router.get("/", response_model=About, include_in_schema=False)
async def get_about():
    doc = await db.about.find_one({}, {"_id": 0})
    if not doc:
        doc = _default_about()
        await db.about.insert_one(doc)
    return doc


@router.put("", response_model=About)
@router.put("/", response_model=About, include_in_schema=False)
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
