import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _uid() -> str:
    return str(uuid.uuid4())


# ---------- Auth ----------
class LoginInput(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    role: str = "admin"
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


# ---------- Projects ----------
class ProjectInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: str = Field(..., max_length=2000)
    tags: List[str] = []
    image_url: Optional[str] = None
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    gradient: Optional[str] = None
    order: int = 0


class Project(ProjectInput):
    id: str = Field(default_factory=_uid)
    created_at: datetime = Field(default_factory=_now)


# ---------- Skills ----------
class SkillInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=60)
    level: int = Field(..., ge=0, le=100)
    icon: str = "Box"
    order: int = 0


class Skill(SkillInput):
    id: str = Field(default_factory=_uid)
    created_at: datetime = Field(default_factory=_now)


# ---------- About ----------
class Stat(BaseModel):
    label: str
    value: str
    suffix: str = ""


class AboutInput(BaseModel):
    name: str
    role: str
    tagline: str
    bio: List[str] = []
    location: str = ""
    email: EmailStr
    available: bool = True
    stats: List[Stat] = []
    socials: Dict[str, str] = {}


class About(AboutInput):
    id: str = Field(default_factory=_uid)
    updated_at: datetime = Field(default_factory=_now)


# ---------- Contact ----------
class ContactInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    subject: Optional[str] = Field(None, max_length=200)
    body: str = Field(..., min_length=1, max_length=5000)


class Message(BaseModel):
    id: str = Field(default_factory=_uid)
    name: str
    email: EmailStr
    subject: Optional[str] = None
    body: str
    read: bool = False
    created_at: datetime = Field(default_factory=_now)


# ---------- AI Chat ----------
class ChatInput(BaseModel):
    session_id: str = Field(..., min_length=4, max_length=80)
    message: str = Field(..., min_length=1, max_length=2000)


class ChatTurn(BaseModel):
    role: str  # "user" | "assistant"
    content: str
    ts: datetime = Field(default_factory=_now)


class ChatResponse(BaseModel):
    session_id: str
    reply: str


# ---------- Analytics ----------
class AnalyticsEventInput(BaseModel):
    type: str = Field(..., max_length=60)  # e.g. page_view, contact_submit, chat_message
    meta: Optional[Dict[str, Any]] = None
    path: Optional[str] = None


class AnalyticsEvent(AnalyticsEventInput):
    id: str = Field(default_factory=_uid)
    ua: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)


class AnalyticsSummary(BaseModel):
    total_events: int
    by_type: Dict[str, int]
    last_7_days: Dict[str, int]
    recent: List[AnalyticsEvent]


model_config = ConfigDict(populate_by_name=True)
