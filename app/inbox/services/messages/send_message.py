# app/inbox/services/messages/send_message.py

from datetime import datetime

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.services.conversations.conversation_service import (
    ConversationService,
)
from app.inbox.services.messages.upload_media import upload_message_media
from app.inbox.serializers.message_serializer import MessageSerializer
from app.inbox.services.conversations.conversation_events import emit_conversation_updated
from app.inbox.services.messages.message_status import ( get_message_status,)

def send_message(
    sender_id,
    receiver_id,
    content=None,
    files=None,
    reply_to_message_id=None,
    media_kind=None,
):
    if not content and not files:
        return {"error": "Message must contain text or media"}, 400

    convo = ConversationService.get_or_create(sender_id, receiver_id)

    if reply_to_message_id:
        parent = Message.query.get(reply_to_message_id)

        if not parent:
            return {"error": "Reply message not found"}, 400

        if parent.conversation_id != convo.id:
            return {"error": "Cannot reply to message in another conversation"}, 400

    msg = Message(
        conversation_id=convo.id,
        sender_id=sender_id,
        content=content,
        backup_content=content,
        edited=False,
        status="sent",
        created_at=datetime.utcnow(),
        reply_to_message_id=reply_to_message_id,
    )

    db.session.add(msg)
    db.session.flush()
    print("AFTER FLUSH:", msg.id)

    # Upload all media (images, videos, audio, metadata, album covers)
    if files:
        upload_message_media(
            msg, files, media_kind_override=media_kind,)
        
    db.session.commit()
    db.session.refresh(msg)

    status, online, in_chat = get_message_status(
        receiver_id,
        convo.id,
        convo.status,)

    msg.status = status

    if status == "delivered" and not msg.delivered_at:
        msg.delivered_at = datetime.utcnow()

    elif status == "read":
        now = datetime.utcnow()

        if not msg.delivered_at:
            msg.delivered_at = now

        if not msg.read_at:
            msg.read_at = now

    db.session.commit()
    db.session.refresh(msg)
    

    serialized = MessageSerializer(msg).to_dict()

    socketio.emit(
        "new_message",
        serialized,
        room=f"user_{receiver_id}",
    )

    socketio.emit(
        "message:new",
        serialized,
        room=f"conversation_{convo.id}",
    )

    emit_conversation_updated(convo.id)

    socketio.emit(
        "message:status",
        {
            "message_id": msg.id,
            "status": msg.status,
        },
        room=f"user_{sender_id}",
    )

    saved = Message.query.get(msg.id)
    print("BEFORE RETURN:", saved.id if saved else None, 
          saved.content if saved else None,)


    return serialized