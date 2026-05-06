# app/realtime/connection_events.py

from flask import request
from flask_socketio import emit, join_room
from app.extensions import socketio
from app.realtime.registry import online_users


@socketio.on("connect")
def handle_connect():
    user_id = request.args.get("user_id")

    if not user_id:
        return False  # reject connection

    online_users[user_id] = request.sid

    # 🔥 user-specific room (IMPORTANT for unread system)
    join_room(f"user_{user_id}")

    emit(
        "user_online",
        {"user_id": user_id},
        broadcast=True
    )


@socketio.on("disconnect")
def handle_disconnect():

    for user_id, sid in list(online_users.items()):

        if sid == request.sid:
            del online_users[user_id]

            emit(
                "user_offline",
                {"user_id": user_id},
                broadcast=True
            )
            break