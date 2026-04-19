from typing import List
from fastapi import APIRouter, HTTPException, Depends

from core.database import db
from core.security import require_admin
from models.schemas import Project, ProjectInput

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=List[Project])
async def list_projects():
    items = await db.projects.find({}, {"_id": 0}).sort("order", 1).to_list(500)
    return items


@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str):
    item = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not item:
        raise HTTPException(404, "Project not found")
    return item


@router.post("", response_model=Project, status_code=201)
async def create_project(body: ProjectInput, _: dict = Depends(require_admin)):
    doc = Project(**body.model_dump()).model_dump()
    await db.projects.insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: str, body: ProjectInput, _: dict = Depends(require_admin)):
    update = body.model_dump()
    res = await db.projects.update_one({"id": project_id}, {"$set": update})
    if res.matched_count == 0:
        raise HTTPException(404, "Project not found")
    doc = await db.projects.find_one({"id": project_id}, {"_id": 0})
    return doc


@router.delete("/{project_id}")
async def delete_project(project_id: str, _: dict = Depends(require_admin)):
    res = await db.projects.delete_one({"id": project_id})
    if res.deleted_count == 0:
        raise HTTPException(404, "Project not found")
    return {"ok": True}
