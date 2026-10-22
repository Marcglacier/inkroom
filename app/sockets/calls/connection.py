from app.inbox.models import Call
from app.inbox.services.calls.marks.mark_call_connection_disconnected import (
    MarkCallConnectionDisconnected,
)
from app.inbox.services.calls.marks.mark_call_connection_reconnected import (
    MarkCallConnectionReconnected,
)
from .helpers.authenticate_socket import (
    get_authenticated_socket_user,
)
from app.inbox.services.settings.blocks.block_policy import BlockPolicy

def register_call_connection(socketio):
    def emit_connection_state(call, status):
        payload = {
            "call_id": call.id,
            "status": status,
        }

        socketio.emit(
            "call:connection",
            payload,
            room=f"user_{call.caller_id}",
        )
        socketio.emit(
            "call:connection",
            payload,
            room=f"user_{call.receiver_id}",
        )

    @socketio.on("call:connection:lost")
    def handle_call_connection_lost(data):
        user_id = get_authenticated_socket_user()

        if user_id is None:
            return {"ok": False, "error": "Socket is not authenticated."}

        call_id = data.get("call_id")

        if not call_id:
            return {"ok": False, "error": "call_id is required."}

        try:
            call_id = int(call_id)
        except (TypeError, ValueError):
            return {"ok": False, "error": "Invalid call_id."}

        call = Call.query.get(call_id)

        if call is None:
            return {"ok": False, "error": "Call not found."}

        if user_id not in (call.caller_id, call.receiver_id):
            return {"ok": False, "error": "Not authorized."}

        if BlockPolicy.blocks_either_user(
            call.caller_id,
            call.receiver_id,
        ):
            return {
                "ok": False,
                "error": "Calling is unavailable.",
            }

        MarkCallConnectionDisconnected(
            call_id=call_id,
            user_id=user_id,
        ).execute()

        call = Call.query.get(call_id)

        if call:
            emit_connection_state(call, "lost")

        return {
            "ok": True,
            "call_id": call_id,
        }

    @socketio.on("call:connection:restored")
    def handle_call_connection_restored(data):
        user_id = get_authenticated_socket_user()

        if user_id is None:
            return {"ok": False, "error": "Socket is not authenticated."}

        call_id = data.get("call_id")

        if not call_id:
            return {"ok": False, "error": "call_id is required."}

        try:
            call_id = int(call_id)
        except (TypeError, ValueError):
            return {"ok": False, "error": "Invalid call_id."}

        call = Call.query.get(call_id)

        if call is None:
            return {"ok": False, "error": "Call not found."}

        if user_id not in (call.caller_id, call.receiver_id):
            return {"ok": False, "error": "Not authorized."}

        if BlockPolicy.blocks_either_user(
            call.caller_id,
            call.receiver_id,
        ):
            return {
                "ok": False,
                "error": "Calling is unavailable.",
            }

        MarkCallConnectionReconnected(
            call_id=call_id,
            user_id=user_id,
        ).execute()

        call = Call.query.get(call_id)

        if call:
            emit_connection_state(call, "restored")

        return {
            "ok": True,
            "call_id": call_id,
        }