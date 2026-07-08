from datetime import datetime
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from app.extensions import db
from app.inbox.models import (
    Message,
    Conversation,
    ConversationClear,
    ConversationParticipant
)
from app.models.user import User
from app.inbox.services.messages.fetch_messages import fetch_messages
from app.inbox.services.messages.fetch_pinned_messages import fetch_pinned
from app.inbox.services.messages.message_reaction_aggregator import build_reactions
from app.storage.service import get_file_url


def build_payload(m, uid):
    payload = {
        "id": m["id"],
        "content": m["content"],
         "media": m.get("media", []),
        "sender_id": m["sender_id"],
        "sender_username": m.get("sender_username"),
        "created_at": m["created_at"],
        "edited": m.get("edited", False),
        "reply_to": m.get("reply_to"),
        "reactions": build_reactions(m["id"]),
        "is_forwarded": m.get("is_forwarded", False),
        "is_pinned": m.get("is_pinned", False),
        "deleted_for_everyone": m.get("deleted_for_everyone", False),
    }

    if m.get("is_sender"):
        payload.update({
            "status": m.get("status"),
            "delivered_at": m.get("delivered_at"),
            "read_at": m.get("read_at"),
        })

    return payload


class ConversationMessagesAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):
        uid = int(get_jwt_identity())
        conversation = Conversation.query.get_or_404(conversation_id)

        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 15))

        # Other participant
        part = (
            ConversationParticipant.query
            .filter_by(conversation_id=conversation_id)
            .filter(ConversationParticipant.user_id != uid)
            .first()
        )
        chamber_user = None
        if part:
            u = User.query.get(part.user_id)
            chamber_user = {
                "id": u.id,
                "name": u.name,
                "username": u.username,
                "avatar":(get_file_url(u.profile_picture) if u.profile_picture else None),
            }

        # Current user participant
        my_participant = (
            ConversationParticipant.query
            .filter_by(conversation_id=conversation_id, user_id=uid)
            .first()
        )
        print("🔥 LAST READ:", my_participant.last_read_message_id if my_participant else None)

        # Delivery receipts
        now = datetime.utcnow()
        (
            Message.query.filter_by(conversation_id=conversation_id)
            .filter(Message.sender_id != uid, Message.delivered_at.is_(None))
            .update({"delivered_at": now, "status": "delivered"}, False)
        )
        db.session.commit()

        

        # Cleared chats
        clear = ConversationClear.query.filter_by(conversation_id=conversation_id, user_id=uid).first()
        cleared_at = clear.cleared_at if clear else None

        msgs = fetch_messages(conversation_id, uid)
        if cleared_at:
            msgs = [m for m in msgs if m["created_at"] > cleared_at]

        # Pagination
        msgs.reverse()
        start, end = (page - 1) * limit, (page * limit)
        page_msgs = list(reversed(msgs[start:end]))

        # Pinned
        pinned = fetch_pinned(conversation_id)
        pinned_ids = {p["message_id"] for p in pinned}
        for m in page_msgs:
            if m["id"] in pinned_ids:
                m["is_pinned"] = True

        return {
            "conversation": {
                "id": conversation_id,
                "status": conversation.status,
                "user": chamber_user,
                "last_read_message_id": my_participant.last_read_message_id if my_participant else None,
            },
            "page": page,
            "limit": limit,
            "has_more": end < len(msgs),
            "pinned_messages": pinned,
            "messages": [build_payload(m, uid) for m in page_msgs],
        }, 200
