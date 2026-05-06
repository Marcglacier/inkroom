# app/realtime/typing_events.py
from flask_socketio import emit
from app.extensions import socketio


# =========================
# USER TYPING
# =========================
@socketio.on("typing")
def handle_typing(data):

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

    emit(
        "user_stopped_typing",
        {
            "user_id": data["user_id"],
            "conversation_id": data["conversation_id"]
        },
        room=f"conversation_{data['conversation_id']}",
        include_self=False
    )