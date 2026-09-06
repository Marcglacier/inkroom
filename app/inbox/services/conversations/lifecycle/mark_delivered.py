from datetime import datetime
from app.extensions import db
from app.inbox.models import Message
from app.inbox.services.conversations.core.conversation_events import ( emit_conversation_updated, )
from app.inbox.services.conversations.core.conversation_guard import ( ConversationGuard, )

def mark_messages_delivered(conversation_id, user_id):
    ConversationGuard.require_participant( conversation_id, user_id, )

    now = datetime.utcnow()

    Message.query.filter(
        Message.conversation_id == conversation_id,
        Message.sender_id != user_id,
        Message.delivered_at.is_(None),
    ).update(
        {
            "delivered_at": now,
            "status": "delivered",
        },
        synchronize_session=False
    )

    db.session.commit()
    emit_conversation_updated(conversation_id)