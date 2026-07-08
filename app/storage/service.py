from minio.error import S3Error
from datetime import timedelta

from app.config import Config
from app.storage.client import minio_client
from app.storage.utils import generate_object_key


def upload_file(file, folder):
    """
    Upload a file to MinIO.

    Returns:
        {
            "object_key": "...",
            "content_type": "...",
            "size": ...,
            "bucket": "..."
        }
    """

    object_key = generate_object_key(folder, file.filename)

    # Calculate file size
    file.stream.seek(0, 2)
    file_size = file.stream.tell()
    file.stream.seek(0)

    try:
        minio_client.put_object(
            bucket_name=Config.MINIO_BUCKET,
            object_name=object_key,
            data=file.stream,
            length=file_size,
            content_type=file.content_type,
        )

        return {
            "object_key": object_key,
            "content_type": file.content_type,
            "size": file_size,
            "bucket": Config.MINIO_BUCKET,
        }

    except S3Error as e:
        raise RuntimeError(f"Failed to upload file: {e}")
    

def get_file_url(object_key: str) -> str:
    """
    Generate a temporary signed URL for a private MinIO object.
    """

    if not object_key:
        return None

    try:
        return minio_client.presigned_get_object(
            bucket_name=Config.MINIO_BUCKET,
            object_name=object_key,
            expires=timedelta(hours=1),
        )

    except S3Error as e:
        raise RuntimeError(f"Failed to generate file URL: {e}")  