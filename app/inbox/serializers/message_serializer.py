from app.common.serializers.base import SerializerMixin
from app.inbox.models.pinned_message import PinnedMessage
from app.inbox.services.messages.message_reaction_aggregator import (build_reactions,)
from app.inbox.serializers.message_media_serializer import MessageMediaSerializer

class MessageSerializer(SerializerMixin):
    def __init__(self, message): self.message = message

    def to_dict(self):
        m = self.message
        return {
            "id": m.id,
            "conversation_id": m.conversation_id,
            "sender_id": m.sender_id,
            "sender_username": m.sender.username if getattr(m, "sender", None) else None,
            "content": m.content,
            "deleted_for_everyone": m.deleted_for_everyone,
            "can_undo_delete": m.can_undo_delete,
            "deleted_for_users": m.deleted_for_users or [],
            "media": [    MessageMediaSerializer(media).to_dict() for media in m.media],
            "created_at": m.created_at.isoformat() + "Z" if m.created_at else None,
            "edited": m.edited,
            "status": m.status,
            "reply_to": {
                "id": m.reply_to.id,
                "content": m.reply_to.content,
                "sender_id": m.reply_to.sender_id,
                "sender_name": m.reply_to.sender.name if m.reply_to.sender else None,
                "sender_username": m.reply_to.sender.username if m.reply_to.sender else None,
            } if m.reply_to else None,
            "is_forwarded": getattr(m, "is_forwarded", False),
            "forwarded_from": {
                "id": m.forwarded_from.id,
                "sender_id": m.forwarded_from.sender_id,
                "sender_name": m.forwarded_from.sender.name if m.forwarded_from.sender else None,
                "sender_username": m.forwarded_from.sender.username if m.forwarded_from.sender else None,
            } if getattr(m, "forwarded_from", None) else None,
            "is_pinned": len(m.pins) > 0,
            "reactions": build_reactions(m.id)
        }
