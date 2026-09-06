# app/sockets/calls/incoming.py


def emit_incoming_call(
    socketio,
    receiver_id: int,
    payload: dict,
) -> None:
    socketio.emit(
        "call:incoming",
        payload,
        room=f"user_{receiver_id}",
    )