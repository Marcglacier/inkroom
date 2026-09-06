# app/inbox/services/conversations/hide_conversation_service.py

from datetime import datetime

from app.extensions import db

from app.inbox.models.conversations.conversation_hide import (
    ConversationHide,
)

from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)


class HideConversationService:

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

        hidden = self._find_hidden()

        if hidden:
            hidden.hidden_at = datetime.utcnow()

        else:
            hidden = ConversationHide(
                conversation_id=self.conversation_id,
                user_id=self.user_id,
                hidden_at=datetime.utcnow(),
            )

            db.session.add(hidden)

        db.session.commit()

        return hidden

    def _find_hidden(self):

        return (
            ConversationHide.query
            .filter_by(
                conversation_id=self.conversation_id,
                user_id=self.user_id,
            )
            .first()
        )