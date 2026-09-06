# app/sockets/calls/initiate.py

from flask import request

from app.extensions import db
from app.models.user import User
from app.inbox.services.calls.mark_call_ringing_service import (
    MarkCallRingingService,
)

from .helpers import (
    get_authenticated_socket_user, resolve_call, 
    get_user_socket_ids, build_call_payload
)

from .incoming import (
    emit_incoming_call,
)

from .status import (
    emit_call_status,
)


def register_call_initiate(socketio):

    @socketio.on("call:initiate")
    def handle_call_initiate(data):

        print(
            "\n📞 CALL INITIATE RECEIVED:",
            data,
        )

        print(
            "📞 CALL INITIATE SID:",
            request.sid,
        )

        # ========================================================
        # AUTHENTICATED USER
        # ========================================================

        caller_id = (
            get_authenticated_socket_user()
        )

        if caller_id is None:
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

        print(
            "📞 SOCKET CALL STATE BEFORE RINGING:",
            {
                "id": call.id,
                "status": call.status,
                "caller_id": call.caller_id,
                "receiver_id": call.receiver_id,
            },
        )

        # ========================================================
        # CALLER OWNERSHIP
        # ========================================================

        if call.caller_id != caller_id:
            print(
                "❌ CALL INITIATE REJECTED:",
                f"user={caller_id}",
                f"call={call.id}",
                f"caller={call.caller_id}",
            )

            return {
                "ok": False,
                "error": "You cannot initiate this call.",
            }

        # ========================================================
        # RECEIVER
        # ========================================================

        receiver_id = call.receiver_id

        caller = User.query.get(
            call.caller_id
        )

        if caller is None:
            return {
                "ok": False,
                "error": "Caller not found.",
            }

        receiver_sockets = get_user_socket_ids(
            receiver_id
        )

        if not receiver_sockets:
            print(
                "📴 RECEIVER NOT CONNECTED:",
                receiver_id,
            )

            return {
                "ok": True,
                "status": call.status,
                "call": build_call_payload(
                    call,
                    caller,
                )["call"],
            }

        # ========================================================
        # CALLING → RINGING
        # ========================================================

        try:
            call = MarkCallRingingService(
                call_id=call.id,
                user_id=caller_id,
            ).execute()

        except Exception as error:
            db.session.rollback()

            print(
                "❌ FAILED TO MARK CALL RINGING:",
                error,
            )

            return {
                "ok": False,
                "error": "Unable to start ringing.",
            }

        # ========================================================
        # PAYLOAD
        # ========================================================

        payload = build_call_payload(
            call,
            caller,
        )

        # ========================================================
        # RECEIVER
        # ========================================================

        emit_incoming_call(
            socketio,
            receiver_id,
            payload,
        )

        # ========================================================
        # CALLER
        # ========================================================

        emit_call_status(
            socketio,
            caller_id,
            payload,
        )

        print(
            "📞 CALL NOW RINGING:",
            f"call={call.id}",
            f"caller={caller_id}",
            f"receiver={receiver_id}",
            f"sockets={receiver_sockets}",
        )

        return {
            "ok": True,
            "status": call.status,
            "call": payload["call"],
        }