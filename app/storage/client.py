from minio import Minio
from app.config import Config


minio_client = Minio(
    endpoint=Config.MINIO_ENDPOINT,
    access_key=Config.MINIO_ACCESS_KEY,
    secret_key=Config.MINIO_SECRET_KEY,
    secure=Config.MINIO_SECURE,
)