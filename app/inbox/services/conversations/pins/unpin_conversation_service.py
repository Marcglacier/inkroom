# app/inbox/services/conversations/unpin_conversation_service.py

from flask import abort

from app.extensions import db

from app.inbox.models.conversations.pinned_conversation import (
    PinnedConversation,
)

from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)


class UnpinConversationService:

    def __init__(
        self,
        conversation_id: int,
        user_id: int,
    ):
        self.conversation_id = conversation_id
        self.user_id = user_id

    def execute(self):

        ConversationGuard.require_participant(
            self.conversation_id,
            self.user_id,
        )

        pin = self._find_pin()

        if not pin:
            abort(
                409,
                description="Conversation is not pinned.",
            )

        db.session.delete(pin)
        db.session.commit()

        return True

    def _find_pin(self):

        return (
            PinnedConversation.query
            .filter_by(
                conversation_id=self.conversation_id,
                user_id=self.user_id,
            )
            .first()
        )