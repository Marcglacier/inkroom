from datetime import datetime
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db, socketio
from app.inbox.models import Message, ConversationClear, ConversationParticipant
from app.models.user import User
from flask import request
from app.inbox.services.messages.fetch_messages import fetch_messages
from app.inbox.services.messages.fetch_pinned_messages import fetch_pinned
from app.inbox.services.messages.message_reaction_aggregator import build_reactions


def build_payload(m, uid):
    p = {
        "id": m["id"],
        "content": m["content"],
        "media_url": m.get("media_url"),
        "media_type": m.get("media_type"),
        "sender_id": m["sender_id"],
        "sender_username": m.get("sender_username"),
        "created_at": m["created_at"],
        "edited": m.get("edited", False),
        "reply_to": m.get("reply_to"),
        "reactions": build_reactions(m["id"]),
        "is_forwarded": m.get("is_forwarded", False),
        "is_pinned": m.get("is_pinned", False),
    }

    if m.get("is_sender"):
        p.update({
            k: m.get(k)
            for k in ["status","delivered_at","read_at"]
        })

    return p



class ConversationMessagesAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        uid = int(get_jwt_identity())


        page = int(request.args.get("page",1))
        limit = int(request.args.get("limit",15))


        # chamber user
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
                "id":u.id,
                "name":u.name,
                "username":u.username,
                "avatar":u.profile_picture
            }



        # receipts
        now = datetime.utcnow()


        Message.query.filter_by(
            conversation_id=conversation_id
        ).filter(
            Message.sender_id != uid,
            Message.delivered_at.is_(None)
        ).update(
            {
                "delivered_at":now,
                "status":"delivered"
            },
            False
        )


        Message.query.filter_by(
            conversation_id=conversation_id
        ).filter(
            Message.sender_id != uid,
            Message.read_at.is_(None)
        ).update(
            {
                "read_at":now,
                "status":"read"
            },
            False
        )


        db.session.commit()



        socketio.emit(
            "messages_updated",
            {
                "conversation_id":conversation_id,
                "user_id":uid
            },
            room=f"conversation_{conversation_id}"
        )



        # cleared
        clear = ConversationClear.query.filter_by(
            conversation_id=conversation_id,
            user_id=uid
        ).first()


        cleared_at = clear.cleared_at if clear else None



        msgs = fetch_messages(
            conversation_id,
            uid
        )


        if cleared_at:
            msgs = [
                m for m in msgs
                if m["created_at"] > cleared_at
            ]



        # newest first pagination
        msgs = msgs[::-1]


        start = (page-1) * limit
        end = start + limit


        page_msgs = msgs[start:end]


        # restore old order
        page_msgs = page_msgs[::-1]



        pinned = fetch_pinned(conversation_id)

        pinned_ids = {
            p["message_id"]
            for p in pinned
        }


        for m in page_msgs:
            if m["id"] in pinned_ids:
                m["is_pinned"] = True



        return {

            "conversation":{
                "id":conversation_id,
                "user":chamber_user
            },

            "page":page,

            "limit":limit,

            "has_more":
                end < len(msgs),


            "pinned_messages":pinned,


            "messages":[
                build_payload(m,uid)
                for m in page_msgs
            ]

        },200