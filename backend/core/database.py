from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DB_NAME]


async def ping() -> bool:
    try:
        await client.admin.command("ping")
        return True
    except Exception:
        return False
