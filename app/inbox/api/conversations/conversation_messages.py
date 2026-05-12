# app/inbox/views/conversation_messages.py

from datetime import datetime
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.models.conversation_clear import ConversationClear

from app.inbox.services.messages.fetch_messages import fetch_messages
from app.inbox.services.messages.fetch_pinned_messages import fetch_pinned
from app.inbox.services.messages.message_reaction_aggregator import build_reactions


def build_payload(message, user_id):

    payload = {
        "id": message["id"],
        "content": message["content"],
        "media_url": message.get("media_url"),
        "media_type": message.get("media_type"),
        "sender_id": message["sender_id"],
        "sender_username": message.get("sender_username"),
        "created_at": message["created_at"],
        "edited": message.get("edited", False),
        "reply_to": message.get("reply_to"),
        "reactions": build_reactions(message["id"]),
        "is_forwarded": message.get("is_forwarded", False),
        "is_pinned": message.get("is_pinned", False),
    }

    # show receipts only to the sender
    if message.get("is_sender"):
        payload.update({
            "status": message.get("status"),
            "delivered_at": message.get("delivered_at"),
            "read_at": message.get("read_at"),
        })

    return payload


class ConversationMessagesAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        user_id = int(get_jwt_identity())

        # mark messages as delivered
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

        # mark messages as read
        Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.read_at.is_(None)
        ).update(
            {
                "read_at": datetime.utcnow(),
                "status": "read"
            },
            synchronize_session=False
        )

        db.session.commit()

        # notify conversation room
        socketio.emit(
            "messages_updated",
            {
                "conversation_id": conversation_id,
                "user_id": user_id
            },
            room=f"conversation_{conversation_id}"
        )

        # check if user cleared the conversation
        clear = ConversationClear.query.filter_by(
            conversation_id=conversation_id,
            user_id=user_id
        ).first()

        cleared_at = clear.cleared_at if clear else None

        # fetch messages
        messages = fetch_messages(conversation_id, user_id)

        if cleared_at:
            messages = [
                m for m in messages
                if m["created_at"] > cleared_at
            ]

        # fetch pinned messages
        pinned = fetch_pinned(conversation_id)
        pinned_ids = {p["message_id"] for p in pinned}

        for m in messages:
            if m["id"] in pinned_ids:
                m["is_pinned"] = True

        return {
            "pinned_messages": pinned,
            "messages": [
                build_payload(m, user_id)
                for m in messages
            ]
        }, 200