"""Update ConnectAI live_url in MongoDB."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.database import db

async def update():
    result = await db.projects.update_one(
        {"title": "ConnectAI"},
        {"$set": {"live_url": "https://chromewebstore.google.com/detail/cjfnhjpheldgcfmipcmibbmlfmpflfij?utm_source=item-share-cb"}}
    )
    print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

asyncio.run(update())
