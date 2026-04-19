from fastapi import APIRouter, HTTPException, Request

from core.rate_limit import limiter
from models.schemas import ChatInput, ChatResponse
from services import ai_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
async def chat(request: Request, body: ChatInput):
    try:
        reply = await ai_service.chat(body.session_id, body.message)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return ChatResponse(session_id=body.session_id, reply=reply)


@router.get("/history/{session_id}")
async def history(session_id: str):
    turns = await ai_service.get_history(session_id)
    return {"session_id": session_id, "history": turns}
