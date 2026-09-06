# app/inbox/services/calls/end_call_service.py

from datetime import datetime

from flask import abort

from app.extensions import db, socketio
from app.inbox.models import Call
from app.inbox.constants.calls import (
    CALL_STATUS_ACCEPTED,
    CALL_STATUS_ENDED,
)
from app.inbox.serializers.call_serializer import CallSerializer
from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)
from app.models.user import User


class EndCallService:

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
        # ONLY ACTIVE CALLS CAN BE ENDED HERE
        # ========================================================

        if call.status != CALL_STATUS_ACCEPTED:
            abort(
                409,
                description="Call is not active.",
            )

        # ========================================================
        # END CALL
        # ========================================================

        call.status = CALL_STATUS_ENDED
        call.ended_at = datetime.utcnow()

        db.session.commit()

        # ========================================================
        # NOTIFY BOTH PARTICIPANTS
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