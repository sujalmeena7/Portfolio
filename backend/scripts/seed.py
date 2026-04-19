"""Seed script: creates admin user + initial portfolio content.

Run:  python /app/backend/scripts/seed.py
"""
import asyncio
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.config import settings  # noqa: E402
from core.database import db  # noqa: E402
from core.security import hash_password  # noqa: E402


PROJECTS = [
    {
        "title": "Nebula Commerce",
        "description": "A WebGL-powered storefront for a luxury audio brand. Product configurator with real-time material shaders and a physics-based cart interaction.",
        "tags": ["Three.js", "React", "GSAP", "Shopify"],
        "gradient": "linear-gradient(135deg, #7b2fff 0%, #00f5ff 100%)",
        "live_url": "https://example.com/nebula",
        "github_url": "https://github.com/example/nebula",
        "order": 1,
    },
    {
        "title": "Cartograph OS",
        "description": "Internal tool for a satellite imagery company. Real-time map rendering, terabyte-scale tile streaming, and collaborative annotation layers.",
        "tags": ["WebGL", "TypeScript", "WebSockets", "Rust"],
        "gradient": "linear-gradient(135deg, #0ea5e9 0%, #7b2fff 100%)",
        "live_url": "https://example.com/cartograph",
        "github_url": "https://github.com/example/cartograph",
        "order": 2,
    },
    {
        "title": "Signal Garden",
        "description": "Generative art platform that turns live audio input into evolving 3D landscapes. Shipped as an installation and a web toy.",
        "tags": ["Three.js", "Web Audio", "GLSL", "Canvas"],
        "gradient": "linear-gradient(135deg, #ec4899 0%, #7b2fff 60%, #00f5ff 100%)",
        "live_url": "https://example.com/signal-garden",
        "github_url": "https://github.com/example/signal-garden",
        "order": 3,
    },
]

SKILLS = [
    {"name": "JavaScript", "level": 95, "icon": "Braces", "order": 1},
    {"name": "React", "level": 92, "icon": "Atom", "order": 2},
    {"name": "Node.js", "level": 85, "icon": "Server", "order": 3},
    {"name": "Three.js", "level": 88, "icon": "Box", "order": 4},
    {"name": "Python", "level": 78, "icon": "Terminal", "order": 5},
    {"name": "Docker", "level": 72, "icon": "Container", "order": 6},
    {"name": "AWS", "level": 70, "icon": "Cloud", "order": 7},
    {"name": "Figma", "level": 82, "icon": "Figma", "order": 8},
]

ABOUT = {
    "name": "ALEX VANTAGE",
    "role": "Creative Developer",
    "tagline": "Crafting immersive digital experiences at the intersection of code, design, and motion.",
    "bio": [
        "I'm a creative developer with 8+ years building production-grade web experiences. I specialise in WebGL, interactive 3D, and performance-obsessed frontends that feel alive.",
        "Previously at agencies and in-house teams across Europe, now freelancing on cinematic brand sites, product interfaces, and creative coding experiments.",
    ],
    "location": "Berlin, DE",
    "email": "hello@alexvantage.dev",
    "available": True,
    "stats": [
        {"label": "Projects", "value": "72", "suffix": "+"},
        {"label": "Years Exp.", "value": "08", "suffix": ""},
        {"label": "Clients", "value": "40", "suffix": "+"},
    ],
    "socials": {
        "github": "https://github.com",
        "linkedin": "https://linkedin.com",
        "twitter": "https://twitter.com",
    },
}


async def seed():
    now = datetime.now(timezone.utc)

    # Admin
    existing_admin = await db.users.find_one({"email": settings.SEED_ADMIN_EMAIL.lower()})
    if not existing_admin:
        await db.users.insert_one({
            "id": str(uuid.uuid4()),
            "email": settings.SEED_ADMIN_EMAIL.lower(),
            "password_hash": hash_password(settings.SEED_ADMIN_PASSWORD),
            "role": "admin",
            "created_at": now,
        })
        print(f"✓ Admin created: {settings.SEED_ADMIN_EMAIL}")
    else:
        print(f"· Admin already exists: {settings.SEED_ADMIN_EMAIL}")

    # Projects
    if await db.projects.count_documents({}) == 0:
        for p in PROJECTS:
            await db.projects.insert_one({"id": str(uuid.uuid4()), "created_at": now, **p})
        print(f"✓ Seeded {len(PROJECTS)} projects")
    else:
        print("· Projects already present")

    # Skills
    if await db.skills.count_documents({}) == 0:
        for s in SKILLS:
            await db.skills.insert_one({"id": str(uuid.uuid4()), "created_at": now, **s})
        print(f"✓ Seeded {len(SKILLS)} skills")
    else:
        print("· Skills already present")

    # About (singleton)
    if await db.about.count_documents({}) == 0:
        await db.about.insert_one({
            "id": str(uuid.uuid4()),
            "updated_at": now,
            **ABOUT,
        })
        print("✓ About seeded")
    else:
        print("· About already present")

    print("\nAll done. Admin login:")
    print(f"  email:    {settings.SEED_ADMIN_EMAIL}")
    print(f"  password: {settings.SEED_ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed())
