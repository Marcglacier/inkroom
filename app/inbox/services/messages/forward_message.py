from datetime import datetime

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.models.message_media import MessageMedia
from app.inbox.services.conversations.conversation_service import (
    ConversationService,
)
from app.inbox.services.messages.message_status import (
    get_message_status,
)


def forward_message(sender_id, message_id, to_user_id):

    original = Message.query.get(message_id)

    if not original:
        return {"error": "Message not found"}, 404

    # =============================
    # GET OR CREATE CONVERSATION
    # =============================
    convo = ConversationService.get_or_create(
        sender_id,
        to_user_id
    )

    # =============================
    # CREATE FORWARDED MESSAGE
    # =============================
    new_msg = Message(
        conversation_id=convo.id,
        sender_id=sender_id,
        content=original.content,
        backup_content=original.content,
        forwarded_from_id=original.id,
        is_forwarded=True,
        edited=False,
        status="sent",
        created_at=datetime.utcnow(),
    )

    db.session.add(new_msg)
    db.session.flush()

    # =============================
    # CLONE MEDIA
    # =============================
    media_urls = []

    original_media = MessageMedia.query.filter_by(
        message_id=original.id
    ).all()

    for media in original_media:

        cloned = MessageMedia(
            message_id=new_msg.id,
            file_url=media.file_url,
            file_type=media.file_type,
        )

        db.session.add(cloned)
        media_urls.append(media.file_url)

    db.session.commit()
    status, online, in_chat = get_message_status(
      to_user_id,
      convo.id,
      convo.status,
    )

    new_msg.status = status

    db.session.commit()
    # =============================
    # BUILD SOCKET PAYLOAD
    # =============================
    payload = new_msg.to_dict()

    payload.update({
        "media": media_urls,
        "reply_to": None,
        "forwarded_from": None,
        "is_pinned": False,
        "reactions": [],
        "created_at": new_msg.created_at.isoformat() + "Z",
    })

    # =============================
    # REALTIME EMIT
    # =============================
    socketio.emit(
        "message:new",
        payload,
        room=f"conversation_{convo.id}",
    )

    socketio.emit(
        "message:status",
        {
            "message_id": new_msg.id,
            "status": status,
        },
        room=f"user_{sender_id}",
    )

    payload["message"] = "forwarded"

    return payload, 201