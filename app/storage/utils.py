from pathlib import Path
from uuid import uuid4


def generate_object_key(folder: str, filename: str) -> str:
    extension = Path(filename).suffix.lower()

    return f"{folder}/{uuid4()}{extension}"