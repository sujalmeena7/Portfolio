from fastapi import APIRouter, Request, Depends, HTTPException
from typing import List

from core.database import db
from core.security import require_admin
from core.rate_limit import limiter
from models.schemas import ContactInput, Message
from services.email_service import send_contact_notification
from core.config import settings

router = APIRouter(tags=["contact"])


@router.post("/contact", response_model=Message, status_code=201)
@limiter.limit("5/minute")
async def submit_contact(request: Request, body: ContactInput):
    msg = Message(**body.model_dump()).model_dump()
    await db.messages.insert_one(msg)
    send_contact_notification(
        to=settings.SEED_ADMIN_EMAIL,
        name=body.name,
        email=body.email,
        subject=body.subject,
        body=body.body,
    )
    msg.pop("_id", None)
    return msg


@router.get("/messages", response_model=List[Message])
async def list_messages(_: dict = Depends(require_admin)):
    items = await db.messages.find({}, {"_id": 0}).sort("created_at", -1).to_list(500)
    return items


@router.patch("/messages/{msg_id}/read", response_model=Message)
async def mark_read(msg_id: str, _: dict = Depends(require_admin)):
    res = await db.messages.update_one({"id": msg_id}, {"$set": {"read": True}})
    if res.matched_count == 0:
        raise HTTPException(404, "Message not found")
    doc = await db.messages.find_one({"id": msg_id}, {"_id": 0})
    return doc


@router.delete("/messages/{msg_id}")
async def delete_message(msg_id: str, _: dict = Depends(require_admin)):
    res = await db.messages.delete_one({"id": msg_id})
    if res.deleted_count == 0:
        raise HTTPException(404, "Message not found")
    return {"ok": True}
