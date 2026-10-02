# app/sockets/calls/end.py

from app.inbox.services.calls.call_room.end_call_service import (
    EndCallService,
)

from .helpers import (
    get_authenticated_socket_user,
)


def register_call_end(socketio):

    @socketio.on("call:end")
    def handle_call_end(data):

        print(
            "\n📞 CALL END RECEIVED:",
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

        try:
            call = EndCallService(
                call_id=call_id,
                user_id=user_id,
            ).execute()

        except Exception as error:
            print(
                "❌ FAILED TO END CALL:",
                error,
            )

            return {
                "ok": False,
                "error": str(error),
            }

        print(
            "📞 CALL ENDED:",
            f"call={call.id}",
            f"user={user_id}",
        )

        return {
            "ok": True,
            "status": call.status,
            "call_id": call.id,
        }