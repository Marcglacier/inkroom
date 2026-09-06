# conversation_visibility_guard.py
from app.inbox.models.conversations.conversation_request import (
    ConversationRequest,
    )


class ConversationVisibilityGuard:

    @staticmethod
    def should_show(
        conversation,
        user_id: int,
    ) -> bool:

        if conversation.status not in (
            "pending",
            "rejected",
        ):
            return True

        request = (
            ConversationRequest.query
            .filter_by(
                conversation_id=conversation.id,
            )
            .first()
        )

        if not request:
            return True

        return request.receiver_id != user_id