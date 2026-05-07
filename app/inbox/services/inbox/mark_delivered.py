# app/inbox/services/inbox/mark_delivered.py

from datetime import datetime
from app.extensions import db
from app.inbox.models.message import Message


def mark_delivered(conversation_id, user_id):

    Message.query.filter(
        Message.conversation_id == conversation_id,
        Message.sender_id != user_id,
        Message.delivered_at.is_(None)
    ).update(
        {
            "delivered_at": datetime.utcnow(),
            "status": "delivered"
        },
        synchronize_session=False
    )

    db.session.commit()