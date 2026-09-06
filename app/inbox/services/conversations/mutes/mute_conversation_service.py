# app/inbox/services/conversations/mutes/mute_conversation_service.py
from datetime import datetime, timedelta

from flask import abort

from app.extensions import db

from app.inbox.models.conversations.muted_conversation import (
    MutedConversation,
)

from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)


class MuteConversationService:

    def __init__(
        self,
        conversation_id: int,
        user_id: int,
        duration: str,
    ):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.duration = duration

    def execute(self):

        ConversationGuard.require_participant(
            self.conversation_id,
            self.user_id,
        )

        mute = self._find_mute()

        if mute:
            abort( 409,
                description="Conversation already muted.",
            )

        mute = self._build_mute()

        db.session.add(mute)
        db.session.commit()

        return mute
    
    def _build_mute(self):

        mute = MutedConversation(
            conversation_id=self.conversation_id,
            user_id=self.user_id,
        )

        if self.duration == "24h":
            mute.muted_until = (
                datetime.utcnow() +
                timedelta(hours=24)
            )

        elif self.duration == "1w":
            mute.muted_until = (
                datetime.utcnow() +
                timedelta(days=7)
            )

        elif self.duration == "always":
            mute.is_always = True

        else:
            abort(
                400,
                description="Invalid mute duration.",
            )

        return mute

    def _find_mute(self):

        return (
            MutedConversation.query
            .filter_by(
                conversation_id=self.conversation_id,
                user_id=self.user_id,
            )
            .first()
        )