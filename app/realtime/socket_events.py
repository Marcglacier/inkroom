# app/realtime/socket_events.py
from flask_socketio import emit, join_room
from datetime import datetime

from app.extensions import db, socketio
from app.inbox.models.message import Message

online_users = {}
# =========================
# JOIN CONVERSATION ROOM
# =========================
@socketio.on("join")
def handle_join(data):
    """
    User joins a conversation room
    """
    room = f"conversation_{data['conversation_id']}"
    join_room(room)


# =========================
# SEND MESSAGE
# =========================
@socketio.on("send_message")
def handle_send_message(data):
    """
    Save message and broadcast to conversation
    """

    msg = Message(
        conversation_id=data["conversation_id"],
        sender_id=data["sender_id"],
        content=data["content"],
        status="sent",
        created_at=datetime.utcnow()
    )

    db.session.add(msg)
    db.session.commit()

    emit(
        "new_message",
        {
            "id": msg.id,
            "conversation_id": msg.conversation_id,
            "sender_id": msg.sender_id,
            "content": msg.content,
            "status": msg.status,
            "created_at": str(msg.created_at)
        },
        room=f"conversation_{msg.conversation_id}"
    )


# =========================
# USER TYPING
# =========================
@socketio.on("typing")
def handle_typing(data):
    """
    Notify others that user is typing
    """

    emit(
        "user_typing",
        {
            "user_id": data["user_id"],
            "conversation_id": data["conversation_id"]
        },
        room=f"conversation_{data['conversation_id']}",
        include_self=False
    )


# =========================
# USER STOPPED TYPING
# =========================
@socketio.on("stop_typing")
def handle_stop_typing(data):
    """
    Notify others that user stopped typing
    """

    emit(
        "user_stopped_typing",
        {
            "user_id": data["user_id"],
            "conversation_id": data["conversation_id"]
        },
        room=f"conversation_{data['conversation_id']}",
        include_self=False
    )