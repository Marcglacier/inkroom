from app.common.serializers.base import SerializerMixin
from app.storage.service import get_file_url


class MessageMediaSerializer(SerializerMixin):

    def __init__(self, media):
        self.media = media

    def to_dict(self):
        return {

            # ---------- Original media ----------
            "id": self.media.id,
            "url": get_file_url(self.media.object_key),
            "object_key": self.media.object_key,
            "filename": self.media.filename,
            "mime_type": self.media.mime_type,
            "size": self.media.size,

            # ---------- General metadata ----------
            "media_kind": self.media.media_kind,
            "created_at": (
                self.media.created_at.isoformat() + "Z"
                if self.media.created_at
                else None
            ),
            "duration": self.media.duration,
            "waveform": self.media.waveform,

            # ---------- Audio metadata ----------
            "title": self.media.title,
            "artist": self.media.artist,
            "album": self.media.album,

            "cover_url": (
                get_file_url(self.media.cover_object_key)
                if self.media.cover_object_key
                else None
            ),

            # ---------- Video metadata ----------
            "video_width": self.media.video_width,
            "video_height": self.media.video_height,

            "thumbnail_url": (
                get_file_url(self.media.thumbnail_object_key)
                if self.media.thumbnail_object_key
                else None
            ),
        }