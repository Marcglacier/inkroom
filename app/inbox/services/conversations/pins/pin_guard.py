# app/inbox/services/conversations/pins/pin_guard.py

from app.inbox.models.conversations.pinned_conversation import (
    PinnedConversation,
)


class PinGuard:

    @staticmethod
    def is_pinned(
        conversation_id: int,
        user_id: int,
    ) -> bool:

        return (
            PinnedConversation.query
            .filter_by(
                conversation_id=conversation_id,
                user_id=user_id,
            )
            .first()
            is not None
        )