# app/inbox/views/conversation_messages.py

from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.services.message_service import MessageService
from app.models.user import User


class ConversationMessagesAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        user_id = int(get_jwt_identity())

        # =============================
        # MARK DELIVERED
        # =============================
        delivered = (
            Message.query
            .filter(
                Message.conversation_id == conversation_id,
                Message.sender_id != user_id,
                Message.delivered_at.is_(None)
            )
            .update(
                {
                    "delivered_at": datetime.utcnow(),
                    "status": "delivered"
                },
                synchronize_session=False
            )
        )

        # =============================
        # MARK READ
        # =============================
        read = (
            Message.query
            .filter(
                Message.conversation_id == conversation_id,
                Message.sender_id != user_id,
                Message.read_at.is_(None)
            )
            .update(
                {
                    "read_at": datetime.utcnow(),
                    "status": "read"
                },
                synchronize_session=False
            )
        )

        db.session.commit()

        # =============================
        # SOCKET EVENTS
        # =============================
        if delivered:
            socketio.emit(
                "messages_delivered",
                {
                    "conversation_id": conversation_id,
                    "user_id": user_id
                },
                room=f"conversation_{conversation_id}"
            )

        if read:
            socketio.emit(
                "messages_read",
                {
                    "conversation_id": conversation_id,
                    "user_id": user_id
                },
                room=f"conversation_{conversation_id}"
            )

        # =============================
        # FETCH MESSAGES
        # =============================
        messages = MessageService.get_messages(
            conversation_id,
            current_user_id=user_id
        )

        results = []

        for m in messages:

            sender = User.query.get(m["sender_id"])

            payload = {
                "id": m["id"],
                "content": m["content"],
                "sender_id": m["sender_id"],
                "sender_username": (
                    sender.username if sender else None
                ),
                "created_at": m["created_at"],
                "edited": m.get("edited", False)
            }

            # =============================
            # ONLY SENDER SEES STATUS
            # =============================
            if m.get("is_sender"):

                payload.update({
                    "status": m.get("status"),
                    "delivered_at": m.get("delivered_at"),
                    "read_at": m.get("read_at")
                })

            results.append(payload)

        return results, 200