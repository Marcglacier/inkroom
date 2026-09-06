# app/sockets/calls/cancel.py

from app.inbox.services.calls.cancel_call_service import (
    CancelCallService,
)

from .helpers import (
    get_authenticated_socket_user,
    resolve_call,
    build_call_payload,
)

from .status import (
    emit_call_status,
)


def register_call_cancel(socketio):

    @socketio.on("call:cancel")
    def handle_call_cancel(data):

        print(
            "\n📞 CALL CANCEL RECEIVED:",
            data,
        )

        # ========================================================
        # AUTHENTICATED USER
        # ========================================================

        user_id = (
            get_authenticated_socket_user()
        )

        if user_id is None:
            return {
                "ok": False,
                "error": "Socket is not authenticated.",
            }

        # ========================================================
        # CALL ID
        # ========================================================

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

        # ========================================================
        # CALL
        # ========================================================

        call = resolve_call(call_id)

        if call is None:
            return {
                "ok": False,
                "error": "Call not found.",
            }

        # ========================================================
        # CANCEL
        # ========================================================

        try:
            call = CancelCallService(
                call_id=call.id,
                user_id=user_id,
            ).execute()

        except Exception as error:
            print(
                "❌ FAILED TO CANCEL CALL:",
                error,
            )

            return {
                "ok": False,
                "error": str(error),
            }

        # ========================================================
        # PAYLOAD
        # ========================================================

        payload = build_call_payload(
            call,
            call.caller,
        )

        # ========================================================
        # CALLER
        # ========================================================

        emit_call_status(
            socketio,
            call.caller_id,
            payload,
        )

        # ========================================================
        # RECEIVER
        # ========================================================

        emit_call_status(
            socketio,
            call.receiver_id,
            payload,
        )

        print(
            "📞 CALL CANCELLED:",
            f"call={call.id}",
            f"caller={call.caller_id}",
            f"receiver={call.receiver_id}",
        )

        return {
            "ok": True,
            "status": call.status,
            "call": payload["call"],
        }