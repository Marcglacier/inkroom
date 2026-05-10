# app/inbox/views/conversation_messages.py
from datetime import datetime
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.models.conversation_clear import ConversationClear
from app.models.user import User

from app.inbox.services.messages.fetch_messages import fetch_messages
from app.inbox.services.messages.fetch_pinned_messages import fetch_pinned
from app.inbox.services.messages.message_reaction_aggregator import build_reactions


def build_payload(message, user_id):
    sender = User.query.get(message["sender_id"])

    payload = {
        "id": message["id"],
        "content": message["content"],
        "sender_id": message["sender_id"],
        "sender_username": sender.username if sender else None,
        "created_at": message["created_at"],
        "edited": message.get("edited", False),
        "reply_to": message.get("reply_to"),
        "reactions": build_reactions(message["id"]),
        "is_forwarded": message.get("is_forwarded", False),
        "is_pinned": message.get("is_pinned", False)
    }

    if message.get("is_sender"):
        payload.update({
            "status": message.get("status"),
            "delivered_at": message.get("delivered_at"),
            "read_at": message.get("read_at")
        })

    return payload


class ConversationMessagesAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        user_id = int(get_jwt_identity())

        # mark delivered
        Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.delivered_at.is_(None)
        ).update({
            "delivered_at": datetime.utcnow(),
            "status": "delivered"
        }, synchronize_session=False)

        # mark read
        Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.read_at.is_(None)
        ).update({
            "read_at": datetime.utcnow(),
            "status": "read"
        }, synchronize_session=False)

        db.session.commit()

        socketio.emit(
            "messages_updated",
            {"conversation_id": conversation_id, "user_id": user_id},
            room=f"conversation_{conversation_id}"
        )

        # check conversation clear
        clear = ConversationClear.query.filter_by(
            conversation_id=conversation_id,
            user_id=user_id
        ).first()

        cleared_at = clear.cleared_at if clear else None

        # fetch normal messages
        messages = fetch_messages(conversation_id, user_id)

        if cleared_at:
            messages = [m for m in messages if m["created_at"] > cleared_at]

        # fetch pinned messages
        pinned_messages = fetch_pinned(conversation_id)

        # mark pinned messages
        pinned_ids = {p["message_id"] for p in pinned_messages}

        for m in messages:
            if m["id"] in pinned_ids:
                m["is_pinned"] = True

        return {
            "pinned_messages": pinned_messages,
            "messages": [build_payload(m, user_id) for m in messages]
        }, 200