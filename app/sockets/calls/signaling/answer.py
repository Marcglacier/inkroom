# app/sockets/calls/signaling/answer.py
from flask import request

from app.sockets.calls.helpers.authenticate_socket import (
    get_authenticated_socket_user,
)
from app.sockets.calls.helpers.resolve_call import (
    resolve_call,
)
from app.sockets.calls.helpers.resolve_participant import (
    get_other_participant_id,
    get_user_socket_ids,
)


def register_call_answer(socketio):

    @socketio.on("call:answer")
    def handle_call_answer(data):

        print(
            "\n📡 CALL ANSWER RECEIVED:",
            data,
        )

        user_id = get_authenticated_socket_user()

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
                "error": "You are not a participant in this call.",
            }

        if call.status != "accepted":
            return {
                "ok": False,
                "error": "Call is not accepted.",
            }

        answer = data.get("answer")

        if not answer:
            return {
                "ok": False,
                "error": "answer is required.",
            }

        participant_id = get_other_participant_id(
            call,
            user_id,
        )

        participant_sockets = get_user_socket_ids(
            participant_id
        )

        if not participant_sockets:
            print(
                "📴 ANSWER TARGET NOT CONNECTED:",
                participant_id,
            )

            return {
                "ok": False,
                "error": "Call participant is not connected.",
            }

        socketio.emit(
            "call:answer",
            {
                "call_id": call.id,
                "answer": answer,
            },
            room=f"user_{participant_id}",
        )

        print(
            "📡 ANSWER RELAYED:",
            f"call={call.id}",
            f"from={user_id}",
            f"to={participant_id}",
        )

        return {
            "ok": True,
        }