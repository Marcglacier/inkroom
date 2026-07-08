from app.extensions import socketio


def emit_presence_status(user_id, online, last_seen=None):
    socketio.emit(
        "presence:status",
        {
            "user_id": user_id,
            "online": online,
            "last_seen": last_seen,
        },
    )