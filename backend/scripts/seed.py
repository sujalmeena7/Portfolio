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
        "title": "LexGuard AI",
        "description": "AI-powered compliance auditor that analyzes legal documents against India's DPDP Act 2023 using tiered RAG + LLM inference. Transforms privacy policies and terms of service into actionable risk assessments with clause-level flagging and remediation suggestions.",
        "tags": ["Python", "FastAPI", "Next.js", "RAG", "Gemini"],
        "gradient": "linear-gradient(135deg, #7b2fff 0%, #00f5ff 100%)",
        "live_url": "https://lexguard-ai-three.vercel.app/",
        "github_url": "https://github.com/sujalmeena7/lexguard-ai",
        "order": 1,
    },
    {
        "title": "Sentinel-SRE",
        "description": "AI-powered root cause analysis platform that ingests Prometheus alerts via webhook, uses RAG (LlamaIndex + Groq) to diagnose incidents, and generates actionable postmortems. Includes chaos simulation, real-time telemetry, and automated incident triage.",
        "tags": ["Python", "FastAPI", "Next.js", "LlamaIndex", "Prometheus", "Docker"],
        "gradient": "linear-gradient(135deg, #0ea5e9 0%, #7b2fff 100%)",
        "live_url": "https://sentinel-sre-zeta.vercel.app",
        "github_url": "https://github.com/sujalmeena7/sentinel-sre",
        "order": 2,
    },
]

SKILLS = [
    {"name": "Python / FastAPI", "level": 95, "icon": "Terminal", "order": 1},
    {"name": "AI Agents / RAG", "level": 92, "icon": "Cpu", "order": 2},
    {"name": "Next.js / React", "level": 85, "icon": "Globe", "order": 3},
    {"name": "Vector DBs", "level": 80, "icon": "Database", "order": 4},
]

ABOUT = {
    "name": "Sujal Meena",
    "role": "Full-Stack AI Engineer",
    "tagline": "Crafting intelligent agentic workflows and high-performance digital systems.",
    "bio": [
        "I am a Computer Science student at PEC Chandigarh and a software developer specializing in AI-driven architectures. I focus on building autonomous agentic workflows and sophisticated RAG pipelines, bridging the gap between raw data and intelligent automation.",
        "My approach combines technical rigor—using stacks like Python, FastAPI, and Next.js—with a commitment to minimalist, high-end design. Whether it's legal tech compliance or performance-heavy hackathon builds, I prioritize clean code and premium user experiences.",
    ],
    "location": "Chandigarh, India",
    "email": "meenasujal60@gmail.com",
    "available": True,
    "stats": [
        {"label": "Projects", "value": "8", "suffix": "+"},
        {"label": "Hackathons", "value": "10", "suffix": "+"},
        {"label": "Technologies", "value": "15", "suffix": "+"},
    ],
    "socials": {
        "github": "https://github.com/sujalmeena7",
        "linkedin": "https://www.linkedin.com/in/sujal-meena-170418371",
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
