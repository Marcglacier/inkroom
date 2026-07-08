from app.common.serializers.base import SerializerMixin
from app.storage.service import get_file_url


class MessageMediaSerializer(SerializerMixin):

    def __init__(self, media):
        self.media = media

    def to_dict(self):
        return {
            "id": self.media.id,
            "url": get_file_url(self.media.object_key),
            "object_key": self.media.object_key,
            "filename": self.media.filename,
            "mime_type": self.media.mime_type,
            "media_kind": self.media.media_kind,   # <-- NEW
            "size": self.media.size,

            # Voice metadata (optional)
            "waveform": self.media.waveform,       # <-- NEW

            # Audio metadata
            "title": self.media.title,
            "artist": self.media.artist,
            "album": self.media.album,
            "duration": self.media.duration,

            # Album artwork
            "cover_url": (
                get_file_url(self.media.cover_object_key)
                if self.media.cover_object_key
                else None
            ),
        }