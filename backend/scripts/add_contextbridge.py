"""Add ContextBridge to the portfolio MongoDB."""
import asyncio
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.config import settings
from core.database import db


NEW_PROJECT = {
    "id": str(uuid.uuid4()),
    "title": "ContextBridge",
    "description": "A local-first, privacy-focused Chrome Extension (Manifest V3) that parses active browser pages into clean Markdown, stores them in IndexedDB, and enables offline RAG/AI chat. Features semantic chunking, full-text search, and integrations with Ollama, Claude, OpenAI, and Gemini.",
    "tags": ["JavaScript", "Chrome Extension", "Manifest V3", "IndexedDB", "RAG", "Ollama"],
    "gradient": "linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%)",
    "live_url": "https://chromewebstore.google.com/detail/contextbridge-%E2%80%93-local-rag/jokgmcedjecppdfnbicfonbmgjpbglko?authuser=0&hl=en-GB",
    "github_url": "https://github.com/sujalmeena7/ContextBridge",
    "image_url": "/contextbridge.png",
    "order": 5,
    "created_at": datetime.now(timezone.utc),
}


async def add_project():
    now = datetime.now(timezone.utc)

    # Check if project already exists
    existing = await db.projects.find_one({"title": NEW_PROJECT["title"]})
    if not existing:
        await db.projects.insert_one(NEW_PROJECT)
        print(f"[SUCCESS] Added project: {NEW_PROJECT['title']}")
    else:
        # Update it to ensure the new URL is saved
        await db.projects.update_one({"title": NEW_PROJECT["title"]}, {"$set": {"live_url": NEW_PROJECT["live_url"]}})
        print(f"[INFO] Project '{NEW_PROJECT['title']}' updated with new live_url")

    # Update stats in about document
    about_doc = await db.about.find_one()
    if about_doc:
        stats = about_doc.get("stats", [])
        for stat in stats:
            if stat.get("label") == "Projects":
                stat["value"] = "10"
                break
        await db.about.update_one({"id": about_doc["id"]}, {"$set": {"stats": stats, "updated_at": now}})
        print("[SUCCESS] Updated Projects stat to 10")
    else:
        print("[INFO] No about document found, skipping stat update")


if __name__ == "__main__":
    asyncio.run(add_project())
