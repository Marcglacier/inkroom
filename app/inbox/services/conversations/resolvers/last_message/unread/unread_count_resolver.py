# unread_count_resolver.py
from app.inbox.models.messages.message import Message

from app.inbox.services.conversations.resolvers.clears.ConversationClearResolver import (
    ConversationClearResolver,
)


class UnreadCountResolver:

    @staticmethod
    def get(
        conversation_id: int,
        user_id: int,
    ) -> int:

        clear = ConversationClearResolver.get(
            conversation_id,
            user_id,
        )

        query = Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.read_at.is_(None),
            Message.deleted_for_everyone.is_(False),
        )

        query = clear.apply(query)

        return query.count()