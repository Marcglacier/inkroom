# app/inbox/services/calls/accept_call_service.py

from datetime import datetime

from flask import abort

from app.extensions import db
from app.inbox.models import Call
from app.inbox.constants.calls import (
    CALL_STATUS_RINGING,
    CALL_STATUS_ACCEPTED,
)
from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)
from app.extensions import db, socketio
from app.inbox.serializers.call_serializer import CallSerializer
from app.models.user import User

class AcceptCallService:

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
        # ONLY THE RECEIVER CAN ACCEPT
        # ========================================================

        if call.receiver_id != self.user_id:
            abort(
                403,
                description="Only the call recipient can accept this call.",
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
        # ACCEPT
        # ========================================================

        now = datetime.utcnow()

        call.status = CALL_STATUS_ACCEPTED
        call.answered_at = now
        call.started_at = now

        db.session.commit()

        # ========================================================
        # NOTIFY CALLER
        # ========================================================

        caller = User.query.get(call.caller_id)

        if caller is None:
            return call

        call_payload = CallSerializer(
            call
        ).to_dict()

        socketio.emit(
            "call:status",
            {
                "call": call_payload,
                "caller": {
                    "id": caller.id,
                    "username": caller.username,
                    "name": caller.name,
                    "avatar": caller.profile_picture,
                },
            },
            room=f"user_{call.caller_id}",
        )

        return call