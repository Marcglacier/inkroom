# app/inbox/services/message_service.py

from datetime import datetime
from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.services.conversation_service import ConversationService


class MessageService:

    # =========================
    # SEND MESSAGE
    # =========================
    @staticmethod
    def send_message(sender_id, receiver_id, content):

        convo = ConversationService.get_or_create(
            sender_id,
            receiver_id
        )

        msg = Message(
            conversation_id=convo.id,
            sender_id=sender_id,
            content=content,
            status="sent",
            delivered_at=None,
            read_at=None
        )

        db.session.add(msg)
        db.session.commit()

        # -------------------------
        # REAL-TIME EVENT
        # -------------------------
        socketio.emit(
            "new_message",
            {
                "message_id": msg.id,
                "conversation_id": convo.id,
                "sender_id": sender_id,
                "content": msg.content,
                "status": "sent"
            },
            room=f"user_{receiver_id}"
        )

        return {
            "message": "sent",
            "message_id": msg.id,
            "conversation_id": convo.id,
            "status": msg.status
        }

    # =========================
    # GET MESSAGES
    # =========================
    @staticmethod
    def get_messages(conversation_id, current_user_id=None):

        msgs = (
            Message.query
            .filter_by(conversation_id=conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )

        results = []

        for m in msgs:

            # =========================
            # DELETE FOR ME
            # =========================
            if (
                m.deleted_for_users
                and current_user_id in m.deleted_for_users
            ):
                continue

            is_sender = (
                m.sender_id == current_user_id
            )

            base = {
                "id": m.id,
                "sender_id": m.sender_id,
                "created_at": m.created_at,
                "edited": m.edited,
                "is_sender": is_sender
            }

            # =========================
            # DELETE FOR EVERYONE
            # =========================
            if m.deleted_for_everyone:

                base.update({
                    "content": "This message was deleted",
                    "deleted": True,
                    "edited": False
                })

                results.append(base)
                continue

            else:
                base["content"] = m.content

            # =========================
            # SENDER VIEW
            # =========================
            if is_sender:

                base.update({
                    "status": m.status,
                    "delivered_at": m.delivered_at,
                    "read_at": m.read_at
                })

            # =========================
            # RECEIVER VIEW
            # =========================
            else:

                # auto-read when receiver opens chat
                if not m.read_at:
                    m.status = "read"
                    m.read_at = datetime.utcnow()

            results.append(base)

        db.session.commit()

        return results