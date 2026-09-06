# app/inbox/services/messages/edit_message.py
from app.inbox.models.conversations.conversation import Conversation
from app.extensions import db, socketio
from app.inbox.services.messages.message_status import (
    get_message_status,
)


def edit_message(message, new_content):

    # =============================
    # PRESERVE ORIGINAL CONTENT
    # =============================
    if not message.backup_content:
        message.backup_content = message.content

    # =============================
    # UPDATE MESSAGE
    # =============================
    message.content = new_content
    message.edited = True

    # =============================
    # RECALCULATE MESSAGE STATUS
    # =============================
    
    convo = Conversation.query.get(message.conversation_id)

    receiver_id = next(
        p.user_id
        for p in convo.participants
        if p.user_id != message.sender_id
    )

    status, _, _ = get_message_status(
      receiver_id,
      message.conversation_id,
      convo.status,
    )

    message.status = status

    db.session.commit()

    # =============================
    # BUILD SOCKET PAYLOAD
    # =============================
    payload = message.to_dict()

    payload["created_at"] = (
        message.created_at.isoformat() + "Z"
    )

    # =============================
    # REALTIME EMIT
    # =============================
    socketio.emit(
        "message:edited",
        payload,
        room=f"conversation_{message.conversation_id}",
    )

    # =============================
    # UPDATE SENDER STATUS
    # =============================
    socketio.emit(
        "message:status",
        {
            "message_id": message.id,
            "status": status,
        },
        room=f"user_{message.sender_id}",
    )

    payload["message"] = "updated"

    return payload