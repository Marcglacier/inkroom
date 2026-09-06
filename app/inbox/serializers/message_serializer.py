# app/inbox/serializers/message_serializer.py
from app.common.serializers.base import SerializerMixin

from app.inbox.services.messages.message_reaction_aggregator import (
    build_reactions,
)

from app.inbox.serializers.message_media_serializer import (
    MessageMediaSerializer,
)

from app.inbox.models.messages.message_link import MessageLink

class MessageSerializer(SerializerMixin):

    def __init__(
        self,
        message,
        viewer_id: int | None = None,
    ):
        self.message = message
        self.viewer_id = viewer_id

    def to_dict(self):
        m = self.message

        return {
            "id": m.id,
            "conversation_id": m.conversation_id,

            "content": m.content,

            "sender_id": m.sender_id,
            "sender_name": (
                m.sender.name
                if m.sender
                else "Deleted User"
            ),

            "sender_username": (
                m.sender.username
                if m.sender
                else "deleted_user"
            ),
            
            "created_at": (
                m.created_at.isoformat() + "Z"
                if m.created_at else None
            ),

            "status": m.status,

            "delivered_at": (
                m.delivered_at.isoformat()
                if m.delivered_at else None
            ),

            "read_at": (
                m.read_at.isoformat()
                if m.read_at else None
            ),

            "edited": m.edited,

            "deleted_for_everyone": (
                m.deleted_for_everyone
            ),

            "can_undo_delete": m.can_undo_delete,
            "deleted_for_users": (
                m.deleted_for_users or []
            ),

            "is_mine": (
                self.viewer_id is not None
                and m.sender_id == self.viewer_id
            ),

            "message_type": m.message_type,
            "system_event": m.system_event,
            "target_message_id": m.target_message_id,

            "reply_to": (
                {
                    "id": m.reply_to.id,
                    "content": m.reply_to.content,
                    "sender_id": m.reply_to.sender_id,
                    "sender_name": (
                        m.reply_to.sender.name
                        if m.reply_to.sender else None
                    ),
                    "sender_username": (
                        m.reply_to.sender.username
                        if m.reply_to.sender else None
                    ),
                }
                if m.reply_to else None
            ),

            "is_forwarded": getattr(
                m,
                "is_forwarded",
                False,
            ),

            "is_pinned": len(m.pins) > 0,

            "reactions": build_reactions(m.id),

            "media": [
                MessageMediaSerializer(media).to_dict()
                for media in m.media
            ],
            "links": [
                link.to_dict()
                for link in m.links
            ],
        }