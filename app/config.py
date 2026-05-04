# config.py
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # PostgreSQL database connection
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:5432@localhost:5432/inkroom_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Authentication
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")

    # Redis (for chat, sessions, pub/sub notifications)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")