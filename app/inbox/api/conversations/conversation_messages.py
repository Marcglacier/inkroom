from app.extensions import db
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
import time
from app.inbox.models import (
    Conversation,
    ConversationClear,
    ConversationParticipant, Message )
from flask import abort
from app.inbox.services.conversations.lifecycle.mark_conversation_read import mark_conversation_read
from app.inbox.services.conversations.lifecycle.mark_delivered import mark_messages_delivered
from app.models.user import User
from app.inbox.services.messages.fetch_messages import fetch_messages
from app.inbox.services.messages.fetch_pinned_messages import fetch_pinned
from app.storage.service import get_file_url
from app.inbox.services.unread.marker  import get_session_unread_marker
from app.inbox.services.conversations.core.conversation_guard import ( ConversationGuard, )

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
        print( "DB VALUE BEFORE ANYTHING:", my_participant.last_read_message_id,)
        print("🔥 DB LAST READ:", my_participant.last_read_message_id)
        

        previous_last_read = get_session_unread_marker(my_participant)
        
        print("🔥 SESSION MARKER:", previous_last_read)
        last_message = (
            Message.query
            .filter_by(conversation_id=conversation_id)
            .order_by(Message.id.desc())
            .first() 
            )
        checkpoint("last_message")
        print("DB LAST MESSAGE:", last_message.id if last_message else None)
        
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
        
        # Read receits
        print("========== BEFORE MARK READ ==========")
        print("previous_last_read:", previous_last_read)
        print("db participant:", my_participant.last_read_message_id)
        mark_conversation_read(conversation_id, uid)
        db.session.refresh(my_participant)
        print("========== AFTER MARK READ ==========")
        print("db participant:", my_participant.last_read_message_id)
        current_last_read = my_participant.last_read_message_id
        
        print("========== RETURN ==========")
        print("previous_last_read:", previous_last_read)
        print( "response value:", previous_last_read)
        print("TOTAL:", time.perf_counter() - request_start)

        payload = {
            "conversation": {
                "id": conversation_id,
                "status": conversation.status,
                "user": chamber_user,
                "last_read_message_id": current_last_read,
                "previous_last_read_message_id": previous_last_read,
            },
            "page": page,
            "limit": limit,
            "has_more": has_more,
            "pinned_messages": pinned,
            "messages": [build_payload(m) for m in msgs],
         }

        checkpoint("payload_build")
        return payload, 200
