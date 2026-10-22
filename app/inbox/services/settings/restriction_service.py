# app/inbox/services/settings/restriction_service.py

from app.extensions import db, socketio
from app.models.settings.user_restriction import UserRestriction
from app.inbox.models import ConversationParticipant, Message
from app.inbox.services.presence.presence_events import (
    emit_presence_snapshot,
    emit_presence_status,
)
from app.inbox.services.messages.read_receipt_policy import (
    ReadReceiptPolicy,
)
from app.sockets.presence_store import online_users, last_seen


class RestrictionService:
    def restrict(self, restricter_id, restricted_id):
        if self._find(restricter_id, restricted_id):
            return False

        db.session.add(
            UserRestriction(
                restricter_id=restricter_id,
                restricted_id=restricted_id,
            )
        )
        db.session.commit()
        self._refresh_presence(restricter_id, restricted_id)
        self._refresh_read_receipts(restricter_id, restricted_id)
        return True

    def unrestrict(self, restricter_id, restricted_id):
        restriction = self._find(restricter_id, restricted_id)
        if not restriction:
            return False

        db.session.delete(restriction)
        db.session.commit()
        self._refresh_presence(restricter_id, restricted_id)
        self._refresh_read_receipts(restricter_id, restricted_id)
        return True

    def _find(self, restricter_id, restricted_id):
        return UserRestriction.query.filter_by(
            restricter_id=restricter_id,
            restricted_id=restricted_id,
        ).first()

    def _refresh_presence(self, user_a_id, user_b_id):
        for user_id in (user_a_id, user_b_id):
            emit_presence_snapshot(user_id)
            emit_presence_status(
                user_id=user_id,
                online=online_users.get(user_id, False),
                last_seen=last_seen.get(user_id),
            )

    def _refresh_read_receipts(self, user_a_id, user_b_id):
        user_ids = {user_a_id, user_b_id}
        participants = ConversationParticipant.query.filter(
            ConversationParticipant.user_id.in_(user_ids)
        ).all()

        conversation_ids = {
            participant.conversation_id
            for participant in participants
        }

        for conversation_id in conversation_ids:
            members = {
                participant.user_id
                for participant in ConversationParticipant.query.filter_by(
                    conversation_id=conversation_id
                ).all()
                if participant.user_id is not None
            }

            if members != user_ids:
                continue

            policy = ReadReceiptPolicy(conversation_id)
            messages = Message.query.filter(
                Message.conversation_id == conversation_id,
                Message.sender_id.in_(user_ids),
                Message.status == "read",
            ).all()

            for message in messages:
                socketio.emit(
                    "message:status",
                    {
                        "conversation_id": conversation_id,
                        "message_id": message.id,
                        "status": policy.message_status(message),
                    },
                    room=f"conversation_{conversation_id}",
                )

    def is_restricted(self, restricter_id, restricted_id):
        return self._find(
            restricter_id,
            restricted_id,
        ) is not None
