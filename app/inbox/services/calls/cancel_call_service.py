# app/inbox/services/calls/cancel_call_service.py

from datetime import datetime

from flask import abort

from app.extensions import db
from app.inbox.models import Call
from app.inbox.constants.calls import (
    CALL_STATUS_CALLING,
     CALL_STATUS_RINGING,
    CALL_STATUS_CANCELLED,
)
from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)


class CancelCallService:

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
        # ONLY THE CALLER CAN CANCEL
        # ========================================================

        if call.caller_id != self.user_id:
            abort(
                403,
                description="Only the caller can cancel this call.",
            )

        # ========================================================
        # VALIDATE CURRENT STATE
        # ========================================================

        if call.status not in (
            CALL_STATUS_CALLING,
            CALL_STATUS_RINGING,
        ):
            abort(
                409,
                description="Call cannot be cancelled in its current state.",
            )

        # ========================================================
        # CANCEL
        # ========================================================

        call.status = CALL_STATUS_CANCELLED
        call.ended_at = datetime.utcnow()

        db.session.commit()

        return call