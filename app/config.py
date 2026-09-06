# app/config.py

import os
from dotenv import load_dotenv


load_dotenv()

class Config:

    # =========================================================
    # APP
    # =========================================================

    ENV = os.getenv("APP_ENV", "development")

    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    if ENV == "production":
        if not SECRET_KEY:
            raise RuntimeError(
                "SECRET_KEY must be set in production."
            )

        if not JWT_SECRET_KEY:
            raise RuntimeError(
                "JWT_SECRET_KEY must be set in production."
            )

    # =========================================================
    # DATABASE
    # =========================================================

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:5432@localhost:5432/inkroom_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================================================
    # DATABASE CONNECTION POOL
    # =========================================================
    DB_POOL_SIZE = int( os.getenv("DB_POOL_SIZE", "10") )

    DB_MAX_OVERFLOW = int( os.getenv("DB_MAX_OVERFLOW", "10") )

    DB_POOL_TIMEOUT = int( os.getenv("DB_POOL_TIMEOUT", "30") )

    DB_POOL_RECYCLE = int( os.getenv("DB_POOL_RECYCLE", "1800") )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": DB_POOL_SIZE,
        "max_overflow": DB_MAX_OVERFLOW,
        "pool_timeout": DB_POOL_TIMEOUT,
        "pool_recycle": DB_POOL_RECYCLE,
        "pool_pre_ping": True,
    }

    # =========================================================
    # REDIS
    # =========================================================

    REDIS_URL = os.getenv( "REDIS_URL", "redis://localhost:6379/0" )

    # =========================================================
    # GOOGLE OAUTH
    # =========================================================

    GOOGLE_CLIENT_ID = os.getenv( "GOOGLE_CLIENT_ID" )

    GOOGLE_CLIENT_SECRET = os.getenv( "GOOGLE_CLIENT_SECRET" )

    # =========================================================
    # MAIL
    # =========================================================

    MAIL_SERVER = os.getenv( "MAIL_SERVER", "smtp.gmail.com" )

    MAIL_PORT = int( os.getenv("MAIL_PORT", "587") )

    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv( "MAIL_USERNAME" )

    MAIL_PASSWORD = os.getenv( "MAIL_PASSWORD" )

    MAIL_DEFAULT_SENDER = os.getenv( "MAIL_USERNAME" )

    ALERT_EMAIL = os.getenv( "ALERT_EMAIL" )

    # =========================================================
    # MINIO
    # =========================================================

    MINIO_ENDPOINT = os.getenv( "MINIO_ENDPOINT" )

    MINIO_ACCESS_KEY = os.getenv( "MINIO_ACCESS_KEY" )

    MINIO_SECRET_KEY = os.getenv( "MINIO_SECRET_KEY" )

    MINIO_BUCKET = os.getenv( "MINIO_BUCKET" )

    MINIO_SECURE = (
        os.getenv( "MINIO_SECURE",  "False" ).lower() == "true"
    )

    # =========================================================
    # SOCKET.IO
    # =========================================================

    SOCKETIO_CORS_ORIGINS = os.getenv(
        "SOCKETIO_CORS_ORIGINS",
        "http://localhost:5173"
    )
    
    SOCKETIO_MESSAGE_QUEUE = os.getenv(
        "SOCKETIO_MESSAGE_QUEUE",
        REDIS_URL,
    )