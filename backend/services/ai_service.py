"""AI service: RAG-style chat using Emergent Universal LLM key.

Strategy (works reliably across multi-turn requests):
  1. Pull live portfolio context from MongoDB (projects, skills, about) on every call.
  2. Persist chat history in MongoDB keyed by session_id.
  3. For each incoming message: fetch recent history (last N turns), construct a rich
     system message containing portfolio context + condensed history, then send the
     new user message through a fresh LlmChat instance (per playbook).
"""
from __future__ import annotations
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from emergentintegrations.llm.chat import LlmChat, UserMessage

from core.config import settings
from core.database import db

log = logging.getLogger("ai")

MAX_HISTORY_TURNS = 12  # last 12 turns (user+assistant pairs counted individually)


async def _build_portfolio_context() -> str:
    about = await db.about.find_one({}, {"_id": 0}) or {}
    projects = await db.projects.find({}, {"_id": 0}).to_list(200)
    skills = await db.skills.find({}, {"_id": 0}).sort("order", 1).to_list(200)

    lines: List[str] = []
    if about:
        lines.append(f"NAME: {about.get('name','')}")
        lines.append(f"ROLE: {about.get('role','')}")
        lines.append(f"TAGLINE: {about.get('tagline','')}")
        lines.append(f"LOCATION: {about.get('location','')}")
        lines.append(f"EMAIL: {about.get('email','')}")
        lines.append(f"AVAILABLE FOR WORK: {about.get('available', True)}")
        if about.get("bio"):
            lines.append("BIO:")
            for b in about["bio"]:
                lines.append(f"  - {b}")

    if skills:
        lines.append("\nSKILLS:")
        for s in skills:
            lines.append(f"  - {s.get('name')} (level {s.get('level')}/100)")

    if projects:
        lines.append("\nPROJECTS:")
        for p in projects:
            tags = ", ".join(p.get("tags", []))
            lines.append(
                f"  * {p.get('title')} — {p.get('description','')} | tags: {tags} | "
                f"live: {p.get('live_url') or 'n/a'} | github: {p.get('github_url') or 'n/a'}"
            )
    return "\n".join(lines) or "(no portfolio data available yet)"


def _system_prompt(portfolio_context: str, recent_history: List[Dict[str, Any]]) -> str:
    hist_block = ""
    if recent_history:
        hist_lines = []
        for turn in recent_history[-MAX_HISTORY_TURNS:]:
            role = turn.get("role", "user").upper()
            hist_lines.append(f"{role}: {turn.get('content','')}")
        hist_block = "\n\nRECENT CONVERSATION:\n" + "\n".join(hist_lines)

    return (
        "You are the AI concierge for a personal developer portfolio. "
        "Answer questions about the developer, recommend relevant projects, "
        "and explain the tech stack. Be concise, warm, and specific \u2014 quote real "
        "project names, skills, and facts only from the PORTFOLIO CONTEXT below. "
        "If asked something you don't know from the context, say so and suggest "
        "the visitor use the contact form. Keep replies under 160 words unless "
        "the user asks for detail. Never invent projects, URLs, or credentials.\n\n"
        f"PORTFOLIO CONTEXT:\n{portfolio_context}{hist_block}"
    )


async def chat(session_id: str, user_text: str) -> str:
    if not settings.EMERGENT_LLM_KEY:
        raise RuntimeError("EMERGENT_LLM_KEY is not configured on the server.")

    # Fetch existing session history
    session = await db.chat_sessions.find_one({"session_id": session_id}) or {
        "session_id": session_id,
        "history": [],
        "created_at": datetime.now(timezone.utc),
    }
    history: List[Dict[str, Any]] = session.get("history", [])

    portfolio_context = await _build_portfolio_context()
    system_msg = _system_prompt(portfolio_context, history)

    chat_client = LlmChat(
        api_key=settings.EMERGENT_LLM_KEY,
        session_id=session_id,
        system_message=system_msg,
    ).with_model(settings.AI_PROVIDER, settings.AI_MODEL)

    try:
        reply = await chat_client.send_message(UserMessage(text=user_text))
        if hasattr(reply, "content"):
            reply_text = reply.content  # type: ignore
        else:
            reply_text = str(reply)
    except Exception as e:  # pragma: no cover
        log.exception("LLM call failed")
        raise RuntimeError(f"AI provider error: {e}")

    # Persist the new turns
    now = datetime.now(timezone.utc)
    history.append({"role": "user", "content": user_text, "ts": now})
    history.append({"role": "assistant", "content": reply_text, "ts": now})

    await db.chat_sessions.update_one(
        {"session_id": session_id},
        {
            "$set": {"history": history, "updated_at": now},
            "$setOnInsert": {"session_id": session_id, "created_at": now},
        },
        upsert=True,
    )

    return reply_text


async def get_history(session_id: str) -> List[Dict[str, Any]]:
    doc = await db.chat_sessions.find_one({"session_id": session_id}, {"_id": 0})
    if not doc:
        return []
    return doc.get("history", [])
