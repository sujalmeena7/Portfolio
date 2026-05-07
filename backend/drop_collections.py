import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.database import db

async def drop():
    await db.projects.delete_many({})
    await db.skills.delete_many({})
    await db.about.delete_many({})
    print("Collections cleared")

asyncio.run(drop())
