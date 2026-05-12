# app/inbox/services/messages/forward_message.py
from datetime import datetime
from app.extensions import db
from app.inbox.models.message import Message
from app.inbox.services.conversations.conversation_service import ConversationService


def forward_message(sender_id, message_id, to_user_id):

    original = Message.query.get(message_id)

    if not original:
        return {"error": "Message not found"}, 404

    # 🔥 ALWAYS derive conversation internally
    convo = ConversationService.get_or_create(sender_id, to_user_id)

    new_msg = Message(
        conversation_id=convo.id,
        sender_id=sender_id,
        content=original.content,
        backup_content=original.content,
        forwarded_from_id=original.id,
        is_forwarded=True,
        created_at=datetime.utcnow(),
        status="sent"
    )

    db.session.add(new_msg)
    db.session.commit()

    return {
        "message": "forwarded",
        "message_id": new_msg.id,
        "conversation_id": convo.id
    }