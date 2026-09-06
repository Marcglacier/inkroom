# app/inbox/services/calls/decline_call_service.py

from datetime import datetime

from flask import abort

from app.extensions import db, socketio
from app.inbox.models import Call
from app.inbox.constants.calls import (
    CALL_STATUS_RINGING,
    CALL_STATUS_DECLINED,
)
from app.inbox.serializers.call_serializer import CallSerializer
from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)
from app.models.user import User


class DeclineCallService:

    def __init__(
        self,
        call_id: int,
        user_id: int,
    ):
        self.call_id = call_id
        self.user_id = user_id

    def execute(self) -> Call:

        # ========================================================
        # FIND CALL
        # ========================================================

        call = Call.query.get(self.call_id)

        if call is None:
            abort(
                404,
                description="Call not found.",
            )

        # ========================================================
        # ACCESS
        # ========================================================

        ConversationGuard.require_participant(
            call.conversation_id,
            self.user_id,
        )

        # ========================================================
        # ONLY THE RECEIVER CAN DECLINE
        # ========================================================

        if call.receiver_id != self.user_id:
            abort(
                403,
                description="Only the call recipient can decline this call.",
            )

        # ========================================================
        # VALIDATE CURRENT STATE
        # ========================================================

        if call.status != CALL_STATUS_RINGING:
            abort(
                409,
                description="Call is not ringing.",
            )

        # ========================================================
        # DECLINE
        # ========================================================

        call.status = CALL_STATUS_DECLINED
        call.ended_at = datetime.utcnow()

        db.session.commit()

        # ========================================================
        # BUILD PAYLOAD
        # ========================================================

        caller = User.query.get(call.caller_id)

        if caller is None:
            return call

        call_payload = CallSerializer(
            call
        ).to_dict()

        payload = {
            "call": call_payload,
            "caller": {
                "id": caller.id,
                "username": caller.username,
                "name": caller.name,
                "avatar": caller.profile_picture,
            },
        }

        # ========================================================
        # NOTIFY BOTH PARTICIPANTS
        # ========================================================

        socketio.emit(
            "call:status",
            payload,
            room=f"user_{call.caller_id}",
        )

        socketio.emit(
            "call:status",
            payload,
            room=f"user_{call.receiver_id}",
        )

        return call