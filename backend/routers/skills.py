from typing import List
from fastapi import APIRouter, HTTPException, Depends

from core.database import db
from core.security import require_admin
from models.schemas import Skill, SkillInput

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=List[Skill])
async def list_skills():
    items = await db.skills.find({}, {"_id": 0}).sort("order", 1).to_list(500)
    return items


@router.post("", response_model=Skill, status_code=201)
async def create_skill(body: SkillInput, _: dict = Depends(require_admin)):
    doc = Skill(**body.model_dump()).model_dump()
    await db.skills.insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.put("/{skill_id}", response_model=Skill)
async def update_skill(skill_id: str, body: SkillInput, _: dict = Depends(require_admin)):
    res = await db.skills.update_one({"id": skill_id}, {"$set": body.model_dump()})
    if res.matched_count == 0:
        raise HTTPException(404, "Skill not found")
    doc = await db.skills.find_one({"id": skill_id}, {"_id": 0})
    return doc


@router.delete("/{skill_id}")
async def delete_skill(skill_id: str, _: dict = Depends(require_admin)):
    res = await db.skills.delete_one({"id": skill_id})
    if res.deleted_count == 0:
        raise HTTPException(404, "Skill not found")
    return {"ok": True}
