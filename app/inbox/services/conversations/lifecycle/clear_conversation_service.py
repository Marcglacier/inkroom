# app/inbox/services/conversations/clear_conversation_service.py

from datetime import datetime

from app.extensions import db

from app.inbox.models.conversations.conversation_clear import (
    ConversationClear,
)

from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)


class ClearConversationService:

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

        clear = self._find_clear()

        if clear:
            clear.cleared_at = datetime.utcnow()

        else:
            clear = ConversationClear(
                conversation_id=self.conversation_id,
                user_id=self.user_id,
            )

            db.session.add(clear)

        db.session.commit()

        return clear

    def _find_clear(self):

        return (
            ConversationClear.query
            .filter_by(
                conversation_id=self.conversation_id,
                user_id=self.user_id,
            )
            .first()
        )