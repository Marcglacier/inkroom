# app/inbox/serializers/message_serializer.py

from app.common.serializers.base import SerializerMixin


class MessageSerializer(SerializerMixin):

    def __init__(self, message):
        self.message = message

    def to_dict(self):

        return {
            # =========================
            # CORE MESSAGE DATA
            # =========================
            "id": self.message.id,
            "conversation_id": self.message.conversation_id,

            "sender_id": self.message.sender_id,
            "sender_username": (
                self.message.sender.username
                if hasattr(self.message, "sender") and self.message.sender
                else None
            ),

            "content": self.message.content,

            # =========================
            # MEDIA SUPPORT (FIXED)
            # =========================
            "media": [
                {
                    "url": f"/media/messages/{m.file_url.split('/')[-1]}",
                    "type": m.file_type
                }
                for m in getattr(self.message, "media", [])
            ],

            # =========================
            # META DATA
            # =========================
            "created_at": (
                self.message.created_at.isoformat()
                if self.message.created_at
                else None
            ),

            "edited": self.message.edited,
            "status": self.message.status,

            # =========================
            # THREADING / FEATURES
            # =========================
            "reply_to": getattr(self.message, "reply_to_message_id", None),
            "is_forwarded": getattr(self.message, "is_forwarded", False),
            "is_pinned": getattr(self.message, "is_pinned", False),

            # =========================
            # FUTURE FEATURES
            # =========================
            "reactions": []
        }