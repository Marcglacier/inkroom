from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
import time
from app.inbox.models import (
    ConversationClear,
    ConversationParticipant, Message )
from app.inbox.services.conversations.lifecycle.mark_delivered import mark_messages_delivered
from app.models.user import User
from app.inbox.services.messages.fetch_messages import fetch_messages
from app.inbox.services.messages.fetch_pinned_messages import fetch_pinned
from app.storage.service import get_file_url
from app.inbox.services.unread.marker  import get_session_unread_marker
from app.inbox.services.conversations.core.conversation_guard import ( ConversationGuard, )
from app.inbox.services.conversations.resolvers.last_message.unread.unread_count_resolver import (
    UnreadCountResolver,
)
from app.models.settings.user_block import UserBlock

def build_payload( m ):

    payload = {
        "id": m["id"],
        "content": m["content"],
        "media": m.get("media", []),
        "links": m.get("links", []),
        "sender_id": m["sender_id"],
        "sender_username": m.get("sender_username"),
        "sender_name": m.get("sender_name"),

        "message_type": m.get("message_type", "text"),
        "system_event": m.get("system_event"),
        "target_message_id": m.get("target_message_id"),
        "call_id": m.get("call_id"),
        "call_type": m.get("call_type"),
        "created_at": m["created_at"],

        "edited": m.get("edited", False),
        "reply_to": m.get("reply_to"),
        "reactions": m.get("reactions", []),
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
        request_start = time.perf_counter()
        def checkpoint(label):
            print(f"{label}: {time.perf_counter() - request_start:.6f}s")
        uid = int(get_jwt_identity())
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 15))
        # Current user participant
        my_participant = ConversationGuard.require_participant( conversation_id, uid, )
        conversation = my_participant.conversation

        checkpoint("my_participant")

        previous_last_read = get_session_unread_marker(my_participant)

        # Other participant
        part = (
            ConversationParticipant.query
            .filter_by(conversation_id=conversation_id)
            .filter(ConversationParticipant.user_id != uid)
            .first()
        )

        blocked_by_me = False

        if part and part.user_id is not None:
            blocked_by_me = UserBlock.query.filter_by(
                blocker_id=uid,
                blocked_id=part.user_id,
            ).first() is not None

        chamber_user = None

        if part and part.user_id is not None:
            other_user_id = part.user_id
            u = User.query.get(other_user_id)

            # Hide the blocker's identity from the person they blocked.
            blocked_viewer = UserBlock.query.filter_by(
                blocker_id=other_user_id,
                blocked_id=uid,
            ).first() is not None

            if blocked_viewer:
                chamber_user = {
                    "id": other_user_id,
                    "name": "Deleted Account",
                    "username": "deleted_account",
                    "avatar": None,
                    "is_deleted": True,
                }
            elif u:
                chamber_user = {
                    "id": u.id,
                    "name": "Deleted Account" if u.is_deleted else u.name,
                    "username": "deleted_account" if u.is_deleted else u.username,
                    "avatar": (
                        None
                        if u.is_deleted
                        else (
                            get_file_url(u.profile_picture)
                            if u.profile_picture
                            else None
                        )
                    ),
                    "is_deleted": u.is_deleted,
                }

        checkpoint("other_participant")



        # Cleared chats
        clear = ConversationClear.query.filter_by(conversation_id=conversation_id, user_id=uid).first()
        cleared_at = clear.cleared_at if clear else None

        offset = (page - 1) * limit
        msgs, has_more = fetch_messages( conversation_id, uid, limit=limit, offset=offset,)

        if cleared_at:
            msgs = [m for m in msgs if m["created_at"] > cleared_at]
        checkpoint("fetch_messages")


        # Pinned
        pinned = fetch_pinned(conversation_id, uid,)
        checkpoint("fetch_pinned")
        pinned_ids = {p["message_id"] for p in pinned}
        for m in msgs:
            if m["id"] in pinned_ids:
                m["is_pinned"] = True

        # Delivery receipts
        t = time.perf_counter()
        mark_messages_delivered( conversation_id, uid)
        print("mark_delivered:", time.perf_counter() - t)

        unread_count = UnreadCountResolver.get(
            conversation_id,
            uid,
        )

        payload = {
            "conversation": {
                "id": conversation_id,
                "status": conversation.status,
                "blocked_by_me": blocked_by_me,
                "user": chamber_user,
                "last_read_message_id": my_participant.last_read_message_id,
                "unread_count": unread_count,
            },
            "page": page,
            "limit": limit,
            "has_more": has_more,
            "pinned_messages": pinned,
            "messages": [build_payload(m) for m in msgs],
         }

        checkpoint("payload_build")
        return payload, 200
