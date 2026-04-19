import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Settings:
    MONGO_URL: str = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME: str = os.environ.get("DB_NAME", "portfolio_db")

    JWT_SECRET: str = os.environ.get("JWT_SECRET", "change-me")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.environ.get("JWT_EXPIRE_MINUTES", "720"))

    SEED_ADMIN_EMAIL: str = os.environ.get("SEED_ADMIN_EMAIL", "admin@portfolio.dev")
    SEED_ADMIN_PASSWORD: str = os.environ.get("SEED_ADMIN_PASSWORD", "Admin@123")

    UPLOAD_DIR: str = os.environ.get("UPLOAD_DIR", str(ROOT_DIR / "uploads"))
    PUBLIC_UPLOAD_BASE: str = os.environ.get("PUBLIC_UPLOAD_BASE", "/api/uploads")

    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    AI_PROVIDER: str = os.environ.get("AI_PROVIDER", "openai")
    AI_MODEL: str = os.environ.get("AI_MODEL", "gpt-4o-mini")

    CORS_ORIGINS: str = os.environ.get("CORS_ORIGINS", "*")


settings = Settings()
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
