# app/notifications/services/socket_events.py

from app.extensions import socketio


def emit_notification(user_id: int, data: dict):
    """
    Send real-time notification to a specific user room
    """

    if not user_id:
        print("⚠️ [SOCKET] Missing user_id, skipping emit")
        return

    room = f"user_{user_id}"

    print(f"🔌 [SOCKET] Emitting to {room}")
    print(f"➡️ Data: {data}")

    socketio.emit(
        "notification:new",
        data,
        room=room
    )