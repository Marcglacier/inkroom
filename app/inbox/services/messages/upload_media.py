from io import BytesIO

from app.extensions import db
from app.inbox.models.messages.message_media import MessageMedia
from app.inbox.services.media.audio_metadata import (
    extract_audio_metadata,
)
from app.inbox.services.media.video.video_metadata import (
    extract_video_metadata,
)
from app.inbox.services.media.video.video_thumbnail import (
    extract_video_thumbnail,
)
from app.storage.folders import chat_folder
from app.storage.service import upload_file


class MemoryFile:
    def __init__(
        self,
        data,
        filename,
        content_type="image/jpeg",
    ):
        self.filename = filename
        self.content_type = content_type
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
    message,
    files,
    media_kind_override=None,
):
    uploaded = []

    for file in files:

        metadata = {}

        media_kind = (
            media_kind_override
            if media_kind_override
            else detect_media_kind(file)
        )

        is_audio = media_kind == "audio"
        is_video = media_kind == "video"

        # ---------------- AUDIO ----------------

        if is_audio:
            metadata = extract_audio_metadata(file)

            print("TITLE:", metadata.get("title"))
            print("HAS COVER:", metadata.get("cover") is not None)

        # ---------------- VIDEO ----------------

        elif is_video:
            metadata = extract_video_metadata(file)
            metadata["thumbnail"] = extract_video_thumbnail(file)
            

        # Metadata readers consume the stream.
        # Reset before uploading the original file.
        file.stream.seek(0)

        # Upload original file
        result = upload_file(
            file=file,
            folder=chat_folder(message.conversation_id),
        )

        media = MessageMedia(
            message_id=message.id,
            object_key=result["object_key"],
            filename=file.filename,
            mime_type=file.content_type,
            size=result["size"],
            media_kind=media_kind,
        )

        # ---------------- AUDIO DATA ----------------

        if is_audio:
            media.title = metadata.get("title")
            media.artist = metadata.get("artist")
            media.album = metadata.get("album")
            media.duration = metadata.get("duration")

            cover = metadata.get("cover")

            print("COVER BYTES:", len(cover) if cover else 0)

            if cover:
                print("⬆️ Uploading album cover...")

                cover_upload = upload_file(
                    file=MemoryFile(
                        cover,
                        filename="cover.jpg",
                    ),
                    folder=chat_folder(message.conversation_id),
                )

                print("✅ Cover uploaded:", cover_upload)

                media.cover_object_key = cover_upload["object_key"]

                print(
                    "💾 Saved cover key:",
                    media.cover_object_key,
                )

        # ---------------- VIDEO DATA ----------------

        if is_video:
            media.duration = metadata.get("duration")
            media.video_width = metadata.get("width")
            media.video_height = metadata.get("height")

            thumbnail = metadata.get("thumbnail")
            print("THUMBNAIL EXISTS:", thumbnail is not None)
            print("THUMBNAIL SIZE:", len(thumbnail) if thumbnail else 0)

            if thumbnail:
                thumbnail_upload = upload_file(
                    file=MemoryFile(
                        thumbnail,
                        filename="thumbnail.jpg",
                    ),
                    folder=chat_folder(message.conversation_id),
                )
                print("THUMBNAIL UPLOAD:", thumbnail_upload)

                media.thumbnail_object_key = (
                    thumbnail_upload["object_key"]
                )

        db.session.add(media)
        uploaded.append(media)

    db.session.commit()

    return uploaded