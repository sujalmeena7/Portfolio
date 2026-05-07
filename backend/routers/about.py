from datetime import datetime, timezone
from fastapi import APIRouter, Depends

from core.database import db
from core.security import require_admin
from models.schemas import About, AboutInput

router = APIRouter(prefix="/about", tags=["about"])


def _default_about() -> dict:
    return About(
        name="Sujal Meena",
        role="Full-Stack AI Engineer",
        tagline="Crafting intelligent agentic workflows and high-performance digital systems.",
        bio=[
            "I am a Computer Science student at PEC Chandigarh and a software developer specializing in AI-driven architectures. I focus on building autonomous agentic workflows and sophisticated RAG pipelines, bridging the gap between raw data and intelligent automation.",
            "My approach combines technical rigor—using stacks like Python, FastAPI, and Next.js—with a commitment to minimalist, high-end design. Whether it's legal tech compliance or performance-heavy hackathon builds, I prioritize clean code and premium user experiences.",
        ],
        location="Chandigarh, India",
        email="meenasujal60@gmail.com",
        available=True,
        stats=[
            {"label": "Projects", "value": "8", "suffix": "+"},
            {"label": "Hackathons", "value": "10", "suffix": "+"},
            {"label": "Technologies", "value": "15", "suffix": "+"},
        ],
        socials={
            "github": "https://github.com/sujalmeena7",
            "linkedin": "https://www.linkedin.com/in/sujal-meena-170418371",
        },
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
