from io import BytesIO

from app.storage.service import upload_file
from app.storage.folders import chat_folder
from app.inbox.models.message_media import MessageMedia
from app.extensions import db
from app.inbox.services.media.audio_metadata import extract_audio_metadata


class MemoryFile:
    def __init__(self, data):
        self.filename = "cover.jpg"
        self.content_type = "image/jpeg"
        self.stream = BytesIO(data)


def detect_media_kind(file):
    mime = file.content_type or ""
    filename = (file.filename or "").lower()

    if mime.startswith("image/"):
        return "image"

    if mime.startswith("video/"):
        return "video"

    if mime.startswith("audio/"):
        return "audio"

    if filename.endswith(
        (
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".txt",
            ".zip",
            ".rar",
        )
    ):
        return "document"

    return "file"        


def upload_message_media(
        message, files, media_kind_override=None,):

    uploaded = []

    for file in files:

        # Read metadata BEFORE uploading because we'll use the uploaded file stream
        metadata = {}

        media_kind = (
            media_kind_override
            if media_kind_override
            else detect_media_kind(file)
        )
        is_audio = media_kind == "audio"

        if is_audio:
            metadata = extract_audio_metadata(file)
            print("TITLE:", metadata.get("title"))
            print("HAS COVER:", metadata.get("cover") is not None)

        # Upload original file
        result = upload_file(
            file=file,
            folder=chat_folder(message.conversation_id)
        )

        media = MessageMedia(
            message_id=message.id,
            object_key=result["object_key"],
            filename=file.filename,
            mime_type=file.content_type,
            size=result["size"],
            media_kind=media_kind
        )

        if is_audio:
            media.title = metadata.get("title")
            media.artist = metadata.get("artist")
            media.album = metadata.get("album")
            media.duration = metadata.get("duration")

            # Upload embedded album cover
            cover = metadata.get("cover")
            print("COVER BYTES:", len(cover) if cover else 0)

            if cover:
                print("⬆️ Uploading album cover...")
                cover_upload = upload_file(
                    file=MemoryFile(cover),
                    folder=chat_folder(message.conversation_id)
                )
                print("✅ Cover uploaded:", cover_upload)
                media.cover_object_key = cover_upload["object_key"]
                print("💾 Saved cover key:", media.cover_object_key)

        db.session.add(media)
        uploaded.append(media)

    db.session.commit()

    return uploaded