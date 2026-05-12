# app/inbox/services/messages/send_message.py

import os
from datetime import datetime
from werkzeug.utils import secure_filename

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.models.message_media import MessageMedia
from app.inbox.services.conversations.conversation_service import ConversationService


UPLOAD_FOLDER = "storage/messages"


def send_message(sender_id, receiver_id, content=None, files=None, reply_to_message_id=None):

    # =============================
    # VALIDATE MESSAGE
    # =============================
    if not content and not files:
        return {"error": "Message must contain text or media"}, 400

    # =============================
    # GET OR CREATE CONVERSATION
    # =============================
    convo = ConversationService.get_or_create(sender_id, receiver_id)

    # =============================
    # VALIDATE REPLY
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
    db.session.flush()  # Get message ID before commit

    media_urls = []

    # =============================
    # HANDLE MEDIA FILES
    # =============================
    if files:

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        for file in files:

            if not file.filename:
                continue

            filename = secure_filename(file.filename)

            path = os.path.join(UPLOAD_FOLDER, filename)

            file.save(path)

            media = MessageMedia(
                message_id=msg.id,
                file_url=path,
                file_type="image"
            )

            db.session.add(media)

            media_urls.append(path)

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
            "media": media_urls,
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
        "media": media_urls,
        "created_at": msg.created_at.isoformat()
    }