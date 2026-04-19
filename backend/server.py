import logging
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from core.config import settings
from core.database import client, ping
from core.rate_limit import limiter
from routers import (
    auth as auth_router,
    projects as projects_router,
    skills as skills_router,
    about as about_router,
    contact as contact_router,
    uploads as uploads_router,
    ai as ai_router,
    analytics as analytics_router,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
log = logging.getLogger("server")

app = FastAPI(
    title="Portfolio API",
    version="1.0.0",
    description="Backend for Alex Vantage's portfolio — JWT auth, projects/skills/about CRUD, contact inbox, AI chat with RAG, analytics.",
)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[settings.CORS_ORIGINS] if settings.CORS_ORIGINS != "*" else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Main API router with /api prefix
api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    ok = await ping()
    return {"service": "portfolio-api", "ok": ok, "version": "1.0.0"}


@api_router.get("/health")
async def health():
    return {"status": "ok", "db": await ping()}


api_router.include_router(auth_router.router)
api_router.include_router(projects_router.router)
api_router.include_router(skills_router.router)
api_router.include_router(about_router.router)
api_router.include_router(contact_router.router)
api_router.include_router(uploads_router.router)
api_router.include_router(ai_router.router)
api_router.include_router(analytics_router.router)

app.include_router(api_router)


@app.on_event("startup")
async def startup():
    log.info("Portfolio API starting — DB=%s, AI=%s/%s", settings.DB_NAME, settings.AI_PROVIDER, settings.AI_MODEL)
    # Indexes
    await client[settings.DB_NAME].users.create_index("email", unique=True)
    await client[settings.DB_NAME].projects.create_index("id", unique=True)
    await client[settings.DB_NAME].skills.create_index("id", unique=True)
    await client[settings.DB_NAME].messages.create_index("id", unique=True)
    await client[settings.DB_NAME].chat_sessions.create_index("session_id", unique=True)
    await client[settings.DB_NAME].analytics_events.create_index("created_at")


@app.on_event("shutdown")
async def shutdown():
    client.close()
