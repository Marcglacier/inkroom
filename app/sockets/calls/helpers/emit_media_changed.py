# app/sockets/calls/helpers/emit_media_changed.py
from app.inbox.serializers.call_serializer import CallSerializer


def emit_media_changed(
    socketio,
    call,
) -> None:
    payload = {
        "call": CallSerializer(
            call
        ).to_dict(),
    }

    socketio.emit(
        "call:media:changed",
        payload,
        room=f"user_{call.caller_id}",
    )

    socketio.emit(
        "call:media:changed",
        payload,
        room=f"user_{call.receiver_id}",
    )