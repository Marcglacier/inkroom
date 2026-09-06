# app/inbox/serializers/conversation_card_serializer.py
from app.common.serializers.base import SerializerMixin


class ConversationCardSerializer(SerializerMixin):

    def __init__(
        self,
        *,
        conversation,
        participant,
        unread,
        is_pinned,
        is_muted,
        mute_until,
        last_message,
    ):
        self.conversation = conversation
        self.participant = participant
        self.unread = unread
        self.is_pinned = is_pinned
        self.is_muted = is_muted
        self.mute_until = mute_until
        self.last_message = last_message

    def to_dict(self):
        return {
            "conversation_id": self.conversation.id,
            "type": self.conversation.type,
            "status": self.conversation.status,

            "user_id": self.participant.other_user_id,
            "username": self.participant.username,
            "name": self.participant.name,
            "avatar": self.participant.avatar,
            "is_deleted": self.participant.is_deleted,

            "unread": self.unread,

            "is_pinned": self.is_pinned,
            "is_muted": self.is_muted,
            "mute_until": self.mute_until,

            "last_message": self.last_message,
        }