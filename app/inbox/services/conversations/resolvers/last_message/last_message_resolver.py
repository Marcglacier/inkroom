# app/inbox/services/conversations/resolvers/last_message_resolver.py

from app.inbox.services.conversations.resolvers.clears.ConversationClearResolver import (
    ConversationClearResolver,
)
from app.inbox.models.messages.message import ( Message, )

from .last_message_result import LastMessageResult


class LastMessageResolver:

    @staticmethod
    def get(
        conversation_id: int,
        user_id: int,
    ) -> LastMessageResult:

        clear = ConversationClearResolver.get(
            conversation_id,
            user_id,
        )

        query = Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.deleted_for_everyone.is_(False),
        )

        query = clear.apply(query)

        last_message = (
            query.order_by(
                Message.created_at.desc()
            ).first()
        )

        return LastMessageResult(
            last_message=last_message,
        )