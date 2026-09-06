# app/inbox/services/calls/mark_call_ringing_service.py

from flask import abort

from app.extensions import db
from app.inbox.models import Call
from app.inbox.constants.calls import (
    CALL_STATUS_CALLING,
    CALL_STATUS_RINGING,
)
from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)


class MarkCallRingingService:

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
        # ONLY THE CALLER CAN MARK IT RINGING
        # ========================================================

        if call.caller_id != self.user_id:
            abort(
                403,
                description="Only the caller can mark this call as ringing.",
            )

        print(
            "📞 SERVICE CALL STATE:",
            {
                "id": call.id,
                "status": call.status,
                "caller_id": call.caller_id,
                "receiver_id": call.receiver_id,
            }
        )
        # ========================================================
        # VALIDATE CURRENT STATE
        # ========================================================

        if call.status != CALL_STATUS_CALLING:
            abort(
                409,
                description="Call is not waiting to ring.",
            )

        # ========================================================
        # MARK RINGING
        # ========================================================

        call.status = CALL_STATUS_RINGING
        print(
            "📞 SERVICE SETTING RINGING:",
            call.id,
        )

        db.session.commit()

        return call