# app/inbox/services/messages/send_message.py

from datetime import datetime

from app.models.user import User
from app.extensions import db, socketio
from app.inbox.models.messages.message import Message
from app.inbox.services.conversations.core.conversation_service import (
    ConversationService,
)
from app.inbox.services.messages.upload_media import upload_message_media
from app.inbox.models.messages.message_link import MessageLink
from app.inbox.services.messages.link_detector import (
    detect_links,
    normalize_url,
)
from app.inbox.serializers.message_serializer import MessageSerializer
from app.inbox.services.conversations.core.conversation_events import (
    emit_conversation_updated,
)
from app.inbox.services.messages.message_status import get_message_status
from app.infrastructure.celery.tasks import (
    fetch_message_link_preview_task,
)

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

    receiver = db.session.get(User, receiver_id)

    if not receiver:
        return {"error": "This account no longer exists"}, 404

    convo = ConversationService.get_or_create(
        sender_id,
        receiver_id,
    )

    if reply_to_message_id:
        parent = Message.query.get(reply_to_message_id)

        if not parent:
            return {"error": "Reply message not found"}, 400

        if parent.conversation_id != convo.id:
            return {
                "error": "Cannot reply to message in another conversation"
            }, 400

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

    # ============================================================
    # MEDIA
    # ============================================================

    if files:
        upload_message_media(
            msg,
            files,
            media_kind_override=media_kind,
        )
    
    # ============================================================
    # LINK DETECTION
    # ============================================================

    detected_links = []

    if content:
        detected_links = detect_links(content)

        for raw_url in detected_links:
            normalized = normalize_url(raw_url)

            print(f"🔗 LINK DETECTED: {raw_url}")
            print(f"🔗 NORMALIZED: {normalized}")

            # Create the link immediately with no preview.
            # Celery will fill the preview in the background.
            link = MessageLink(
                message_id=msg.id,
                url=raw_url,
                normalized_url=normalized,
            )

            db.session.add(link)    
    # ============================================================
    # SAVE MESSAGE
    # ============================================================

    db.session.commit()
    db.session.refresh(msg)

    # ============================================================
    # QUEUE LINK PREVIEWS
    # ============================================================

    for raw_url in detected_links:
        normalized = normalize_url(raw_url)

        fetch_message_link_preview_task.delay(
            message_id=msg.id,
            raw_url=raw_url,
            normalized_url=normalized,
        )

    # ============================================================
    # MESSAGE STATUS
    # ============================================================

    status, online, in_chat = get_message_status(
        receiver_id,
        convo.id,
        convo.status,
    )

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

    # ============================================================
    # SERIALIZE
    # ============================================================

    serialized = MessageSerializer(msg).to_dict()

    # ============================================================
    # SOCKET EVENTS
    # ============================================================

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

    print(
        "BEFORE RETURN:",
        saved.id if saved else None,
        saved.content if saved else None,
    )

    return serialized