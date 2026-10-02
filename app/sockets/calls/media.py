# app/sockets/calls/media.py


from .helpers import (
    get_authenticated_socket_user,
    resolve_call, emit_media_changed,
)

from app.inbox.services.calls.connections.media_switch_state import (
    media_switch_state,
)


def emit_media_request(
    socketio,
    user_id: int,
    payload: dict,
) -> None:
    socketio.emit(
        "call:media:request",
        payload,
        room=f"user_{user_id}",
    )


def register_call_media(socketio):

    @socketio.on("call:media:request")
    def handle_media_request(data):

        print(
            "\n📹 MEDIA REQUEST RECEIVED:",
            data,
        )

        user_id = (
            get_authenticated_socket_user()
        )

        if user_id is None:
            return {
                "ok": False,
                "error": "Socket is not authenticated.",
            }

        call_id = data.get("call_id")

        if not call_id:
            return {
                "ok": False,
                "error": "call_id is required.",
            }

        try:
            call_id = int(call_id)

        except (TypeError, ValueError):
            return {
                "ok": False,
                "error": "Invalid call_id.",
            }

        call = resolve_call(call_id)

        if call is None:
            return {
                "ok": False,
                "error": "Call not found.",
            }

        if user_id not in (
            call.caller_id,
            call.receiver_id,
        ):
            return {
                "ok": False,
                "error": "User is not part of this call.",
            }

        if call.status != "accepted":
            return {
                "ok": False,
                "error": "Call is not active.",
            }

        requested_type = data.get(
            "requested_type"
        )

        if requested_type not in ("audio", "video"):
            return {
                "ok": False,
                "error": "Invalid media request.",
            }

        if media_switch_state.exists(call.id):
            return {
                "ok": False,
                "error": (
                    "A media switch request "
                    "is already pending."
                ),
            }

        media_switch_state.set(
            call_id= call.id,
            requested_type=requested_type,
            requested_by=user_id,
        )

        if user_id == call.caller_id:
            target_user_id = call.receiver_id
        else:
            target_user_id = call.caller_id

        payload = {
            "call_id": call.id,
            "requested_type": requested_type,
            "requested_by": user_id,
        }

        emit_media_request(
            socketio,
            target_user_id,
            payload,
        )

        print(
            "📹 MEDIA REQUEST SENT:",
            f"call={call.id}",
            f"from={user_id}",
            f"to={target_user_id}",
            f"type={requested_type}",
        )

        return {
            "ok": True,
            "call_id": call.id,
            "requested_type": requested_type,
        }

    @socketio.on("call:media:respond")
    def handle_media_response(data):

        print(
            "\n📹 MEDIA RESPONSE RECEIVED:",
            data,
        )

        user_id = (
            get_authenticated_socket_user()
        )

        if user_id is None:
            return {
                "ok": False,
                "error": "Socket is not authenticated.",
            }

        call_id = data.get("call_id")

        if not call_id:
            return {
                "ok": False,
                "error": "call_id is required.",
            }

        try:
            call_id = int(call_id)

        except (TypeError, ValueError):
            return {
                "ok": False,
                "error": "Invalid call_id.",
            }

        call = resolve_call(call_id)

        if call is None:
            return {
                "ok": False,
                "error": "Call not found.",
            }

        if user_id not in (
            call.caller_id,
            call.receiver_id,
        ):
            return {
                "ok": False,
                "error": "User is not part of this call.",
            }

        if call.status != "accepted":
            return {
                "ok": False,
                "error": "Call is not active.",
            }

        response = data.get("response")

        if response not in (
            "accepted",
            "declined",
        ):
            return {
                "ok": False,
                "error": "Invalid media response.",
            }

        if not media_switch_state.exists(call.id):
            return {
                "ok": False,
                "error": "No media switch request is pending.",
            }

        request_state = media_switch_state.get(
            call.id
        )

        if request_state is None:
            return {
                "ok": False,
                "error": "Media switch request not found.",
            }
        requester_id = request_state["requested_by"]

        if response == "accepted":
            call.call_type = request_state["requested_type"]
            emit_media_changed(
                socketio, call,
            )

        media_switch_state.clear(call.id)

        socketio.emit(
            "call:media:response",
            {
                "call_id": call.id,
                "response": response,     
            },
            room=f"user_{requester_id}",
        )

        return {
            "ok": True,
            "call_id": call.id,
            "response": response,
        }

