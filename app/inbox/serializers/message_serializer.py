# app/inbox/serializers/message_serializer.py
from app.common.serializers.base import SerializerMixin


class MessageSerializer(SerializerMixin):

    def __init__(self, message):
        self.message = message

    def to_dict(self):
        return {
            "message_id": self.message.id,
            "content": self.message.content,
            "conversation_id": self.message.conversation_id,
            "sender_id": self.message.sender_id,
            "created_at": self.message.created_at.isoformat() if self.message.created_at else None,
            "edited": self.message.edited,
            "status": self.message.status
        }