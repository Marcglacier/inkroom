# app/sockets/calls/status.py


def emit_call_status(
    socketio,
    user_id: int,
    payload: dict,
) -> None:
    socketio.emit(
        "call:status",
        payload,
        room=f"user_{user_id}",
    )