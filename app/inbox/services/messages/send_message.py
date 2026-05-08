# app/inbox/services/messages/send_message.py

from datetime import datetime

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.services.conversations.conversation_service import ConversationService


def send_message(sender_id, receiver_id, content, reply_to_message_id=None):

    # =============================
    # GET OR CREATE CONVERSATION
    # =============================
    convo = ConversationService.get_or_create(sender_id, receiver_id)

    # =============================
    # VALIDATE REPLY (🔥 FIX)
    # =============================
    if reply_to_message_id:
        parent = Message.query.get(reply_to_message_id)

        if not parent:
            return {"error": "Reply message not found"}, 400

        if parent.conversation_id != convo.id:
            return {"error": "Cannot reply to message in another conversation"}, 400

    # =============================
    # CREATE MESSAGE
    # =============================
    msg = Message(
        conversation_id=convo.id,
        sender_id=sender_id,
        content=content,
        backup_content=content,
        edited=False,
        status="sent",
        delivered_at=None,
        read_at=None,
        created_at=datetime.utcnow(),
        reply_to_message_id=reply_to_message_id
    )

    db.session.add(msg)
    db.session.commit()

    # =============================
    # REALTIME EMIT
    # =============================
    socketio.emit(
        "new_message",
        {
            "message_id": msg.id,
            "conversation_id": convo.id,
            "sender_id": sender_id,
            "content": msg.content,
            "reply_to_message_id": msg.reply_to_message_id,
            "status": msg.status,
            "created_at": msg.created_at.isoformat(),
            "edited": msg.edited
        },
        room=f"user_{receiver_id}"
    )

    return {
        "message": "sent",
        "message_id": msg.id,
        "conversation_id": convo.id,
        "status": msg.status,
        "reply_to_message_id": msg.reply_to_message_id,
        "created_at": msg.created_at.isoformat()
    }