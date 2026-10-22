from app.extensions import db, socketio
from app.inbox.models import Message
from app.inbox.services.conversations.core.conversation_events import (
    emit_conversation_updated,
)
from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)
from app.inbox.services.messages.read_receipt_policy import (
    ReadReceiptPolicy,
)

class MarkConversationReadService:

    def execute(
        self,
        conversation_id: int,
        user_id: int,
        through_message_id: int,
    ) -> int | None:

        participant = ConversationGuard.require_participant(
            conversation_id,
            user_id,
        )

        messages = (
            Message.query
            .filter(
                Message.conversation_id == conversation_id,
                Message.sender_id != user_id,
                Message.id <= through_message_id,
                Message.read_at.is_(None),
            )
            .all()
        )

        if not messages:
            return participant.last_read_message_id

        Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.id <= through_message_id,
            Message.read_at.is_(None),
        ).update(
            {
                "read_at": db.func.now(),
                "status": "read",
            },
            synchronize_session=False,
        )

        highest_read = max(message.id for message in messages)

        if (
            participant.last_read_message_id is None
            or highest_read > participant.last_read_message_id
        ):
            participant.last_read_message_id = highest_read

        db.session.commit()

        receipt_visible = ReadReceiptPolicy(
            conversation_id
        ).visible

        if receipt_visible:
            for message in messages:
                socketio.emit(
                    "message:status",
                    {
                        "conversation_id": conversation_id,
                        "message_id": message.id,
                        "status": "read",
                    },
                    room=f"conversation_{conversation_id}",
                )

        socketio.emit(
            "conversation:read",
            {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "last_read_message_id": (
                    participant.last_read_message_id
                ),
            },
            room=f"user_{user_id}",
        )

        emit_conversation_updated(conversation_id)

        return participant.last_read_message_id