# app/inbox/services/conversations/mutes/mute_guard.py

from datetime import datetime

from app.extensions import db

from app.inbox.models.conversations.muted_conversation import (
    MutedConversation,
)


class MuteGuard:

    @staticmethod
    def get_status(
        conversation_id: int,
        user_id: int,
    ):
        mute = (
            MutedConversation.query
            .filter_by(
                conversation_id=conversation_id,
                user_id=user_id,
            )
            .first()
        )

        if not mute:
            return False, None

        # Permanent mute
        if mute.is_always:
            return True, None

        # Safety check
        if not mute.muted_until:
            db.session.delete(mute)
            db.session.commit()
            return False, None

        # Expired
        if mute.muted_until <= datetime.utcnow():
            db.session.delete(mute)
            db.session.commit()
            return False, None

        return (
            True,
            mute.muted_until.isoformat() + "Z",
        )