# app/inbox/services/conversations/mutes/unmute_conversation_service.py
from flask import abort

from app.extensions import db

from app.inbox.models.conversations.muted_conversation import (
    MutedConversation,
)

from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)


class UnmuteConversationService:

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

        mute = self._find_mute()

        if not mute:
            abort(
                404,
                description="Conversation is not muted.",
            )

        db.session.delete(mute)
        db.session.commit()

    def _find_mute(self):

        return (
            MutedConversation.query
            .filter_by(
                conversation_id=self.conversation_id,
                user_id=self.user_id,
            )
            .first()
        )