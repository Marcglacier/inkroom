from flask import abort

from app.inbox.models.conversations.conversation_participant import (
    ConversationParticipant,
)


class ConversationGuard:

    @staticmethod
    def require_participant(
        conversation_id: int,
        user_id: int,
    ) -> ConversationParticipant:

        participant = (
            ConversationParticipant.query
            .filter_by(
                conversation_id=conversation_id,
                user_id=user_id,
            )
            .first()
        )

        if participant is None:
            abort(
                404,
                description="Conversation not found.",
            )

        return participant