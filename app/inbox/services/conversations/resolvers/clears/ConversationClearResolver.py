from app.inbox.models.conversations.conversation_clear import (
    ConversationClear,
    )

from .conversation_clear_result import (
    ConversationClearResult,
)


class ConversationClearResolver:

    @staticmethod
    def get(
        conversation_id: int,
        user_id: int,
    ) -> ConversationClearResult:

        clear = (
            ConversationClear.query
            .filter_by(
                conversation_id=conversation_id,
                user_id=user_id,
            )
            .first()
        )

        return ConversationClearResult(clear)