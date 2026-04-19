from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends

from core.database import db
from core.security import (
    verify_password, create_access_token, get_current_user, hash_password,
)
from models.schemas import LoginInput, TokenResponse, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginInput):
    user = await db.users.find_one({"email": body.email.lower()})
    if not user or not verify_password(body.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=user["email"], role=user.get("role", "admin"))
    return TokenResponse(
        access_token=token,
        user=UserPublic(
            id=user["id"],
            email=user["email"],
            role=user.get("role", "admin"),
            created_at=user["created_at"],
        ),
    )


@router.get("/me", response_model=UserPublic)
async def me(user: dict = Depends(get_current_user)):
    return UserPublic(**user)


@router.post("/register-admin", response_model=UserPublic, include_in_schema=False)
async def register_admin_first_time(body: LoginInput):
    """One-time bootstrap: only works if no admin exists yet."""
    existing = await db.users.find_one({"role": "admin"})
    if existing:
        raise HTTPException(status_code=403, detail="Admin already exists")
    import uuid
    doc = {
        "id": str(uuid.uuid4()),
        "email": body.email.lower(),
        "password_hash": hash_password(body.password),
        "role": "admin",
        "created_at": datetime.now(timezone.utc),
    }
    await db.users.insert_one(doc)
    return UserPublic(id=doc["id"], email=doc["email"], role="admin", created_at=doc["created_at"])
