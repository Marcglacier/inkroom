# app/realtime/message_events.py
from flask_socketio import emit, join_room
from datetime import datetime

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.realtime.registry import online_users


# =========================
# JOIN USER ROOM (IMPORTANT)
# =========================
@socketio.on("join_user")
def handle_join_user(data):
    join_room(f"user_{data['user_id']}")


# =========================
# JOIN CONVERSATION ROOM
# =========================
@socketio.on("join_conversation")
def handle_join_conversation(data):
    join_room(f"conversation_{data['conversation_id']}")


# =========================
# SEND MESSAGE (REAL-TIME CORE)
# =========================
@socketio.on("send_message")
def handle_send_message(data):

    msg = Message(
        conversation_id=data["conversation_id"],
        sender_id=data["sender_id"],
        content=data["content"],
        status="sent",
        created_at=datetime.utcnow()
    )

    db.session.add(msg)
    db.session.commit()

    receiver_id = data["receiver_id"]

    # -------------------------
    # SEND TO RECEIVER
    # -------------------------
    emit(
        "new_message",
        {
            "message_id": msg.id,
            "conversation_id": msg.conversation_id,
            "sender_id": msg.sender_id,
            "content": msg.content,
            "status": "sent",
            "created_at": str(msg.created_at)
        },
        room=f"user_{receiver_id}"
    )

    # -------------------------
    # ALSO UPDATE SENDER UI
    # -------------------------
    emit(
        "message_sent",
        {
            "message_id": msg.id,
            "conversation_id": msg.conversation_id,
            "status": "sent"
        },
        room=f"user_{msg.sender_id}"
    )