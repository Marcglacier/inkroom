# app/inbox/services/messages/send_message.py
from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.services.conversations.conversation_service import ConversationService


def send_message(sender_id, receiver_id, content):

    convo = ConversationService.get_or_create(sender_id, receiver_id)

    msg = Message(
        conversation_id=convo.id,
        sender_id=sender_id,
        content=content,
        status="sent",
        delivered_at=None,
        read_at=None
    )

    db.session.add(msg)
    db.session.commit()

    socketio.emit(
        "new_message",
        {
            "message_id": msg.id,
            "conversation_id": convo.id,
            "sender_id": sender_id,
            "content": msg.content,
            "status": "sent"
        },
        room=f"user_{receiver_id}"
    )

    return {
        "message": "sent",
        "message_id": msg.id,
        "conversation_id": convo.id,
        "status": msg.status
    }