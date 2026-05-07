# app/inbox/views/conversation_messages.py

from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.models.conversation_clear import ConversationClear
from app.models.user import User

from app.inbox.services.messages.fetch_messages import fetch_messages


class ConversationMessagesAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        user_id = int(get_jwt_identity())

        # =============================
        # MARK DELIVERED
        # =============================
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

        # =============================
        # MARK READ
        # =============================
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

        # =============================
        # SOCKET EVENTS
        # =============================
        socketio.emit(
            "messages_updated",
            {
                "conversation_id": conversation_id,
                "user_id": user_id
            },
            room=f"conversation_{conversation_id}"
        )

        # =============================
        # CHECK CLEAR CHAT
        # =============================
        clear = ConversationClear.query.filter_by(
            conversation_id=conversation_id,
            user_id=user_id
        ).first()

        # =============================
        # FETCH MESSAGES
        # =============================
        messages = fetch_messages(
            conversation_id,
            current_user_id=user_id
        )

        # hide messages before clear time
        if clear:
            messages = [
                m for m in messages
                if m["created_at"] > clear.cleared_at
            ]

        results = []

        for m in messages:

            sender = User.query.get(m["sender_id"])

            payload = {
                "id": m["id"],
                "content": m["content"],
                "sender_id": m["sender_id"],
                "sender_username": sender.username if sender else None,
                "created_at": m["created_at"],
                "edited": m.get("edited", False)
            }

            # sender sees full tracking
            if m.get("is_sender"):
                payload.update({
                    "status": m.get("status"),
                    "delivered_at": m.get("delivered_at"),
                    "read_at": m.get("read_at")
                })

            results.append(payload)

        return results, 200