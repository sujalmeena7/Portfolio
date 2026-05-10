"""Add Tab Hibernator Pro to the portfolio MongoDB."""
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
    "title": "Tab Hibernator Pro",
    "description": "High-performance, privacy-first Chrome extension that intelligently suspends inactive tabs to reclaim system memory. Built on Manifest V3 with a smart exclusion engine that detects audio, video, and active form inputs to ensure zero data loss while keeping the browser blazing fast.",
    "tags": ["JavaScript", "Chrome Extension", "Manifest V3", "Performance"],
    "gradient": "linear-gradient(135deg, #4f46e5 0%, #818cf8 100%)",
    "live_url": "https://github.com/sujalmeena7/Tab-Hibernator-Pro",
    "github_url": "https://github.com/sujalmeena7/Tab-Hibernator-Pro",
    "image_url": None,
    "order": 4,
    "created_at": datetime.now(timezone.utc),
}


async def add_project():
    now = datetime.now(timezone.utc)

    # Check if project already exists
    existing = await db.projects.find_one({"title": NEW_PROJECT["title"]})
    if existing:
        print(f"· Project '{NEW_PROJECT['title']}' already exists")
        return

    await db.projects.insert_one(NEW_PROJECT)
    print(f"✓ Added project: {NEW_PROJECT['title']}")

    # Update stats in about document
    about_doc = await db.about.find_one()
    if about_doc:
        stats = about_doc.get("stats", [])
        for stat in stats:
            if stat.get("label") == "Projects":
                stat["value"] = "9"
                break
        await db.about.update_one({"id": about_doc["id"]}, {"$set": {"stats": stats, "updated_at": now}})
        print("✓ Updated Projects stat to 9")
    else:
        print("· No about document found, skipping stat update")


if __name__ == "__main__":
    asyncio.run(add_project())
