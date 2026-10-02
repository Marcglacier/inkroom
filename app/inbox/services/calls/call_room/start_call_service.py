# app/inbox/services/calls/start_call_service.py

from flask import abort

from app.extensions import db
from app.inbox.models import Call
from app.inbox.constants.calls import (
    CALL_TYPE_AUDIO,
    CALL_TYPE_VIDEO,
    CALL_STATUS_CALLING,
    CALL_STATUS_RINGING,
    CALL_STATUS_ACCEPTED,
)
from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)
from app.inbox.services.inbox.get_other_user import (
    get_other_user,
)


class StartCallService:

    def __init__(
        self,
        conversation_id: int,
        user_id: int,
        call_type: str,
    ):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.call_type = call_type

    def execute(self) -> Call:

        # INPUT VALIDATION 
           
        if self.conversation_id is None:
            abort(
                400,
                description="conversation_id is required.",
            )

        if not self.call_type:
            abort(
                400,
                description="call_type is required.",
            )   

        # ACCESS

        ConversationGuard.require_participant(
            self.conversation_id,
            self.user_id,
        )

        # VALIDATE CALL TYPE
        if self.call_type not in {
            CALL_TYPE_AUDIO,
            CALL_TYPE_VIDEO,
        }:
            abort(
                400,
                description="Invalid call type.",
            )

        # RESOLVE RECEIVER

        receiver = get_other_user(
            self.conversation_id,
            self.user_id,
        )

        if receiver is None:
            abort(
                400,
                description="Conversation has no other participant.",
            )

        # CHECK ACTIVE CALL

        active_call = (
            Call.query
            .filter(
                Call.conversation_id
                == self.conversation_id,
                Call.status.in_(
                    [
                        CALL_STATUS_CALLING,
                        CALL_STATUS_RINGING,
                        CALL_STATUS_ACCEPTED,
                    ]
                ),
            )
            .first()
        )

        if active_call:
            abort(
                409,
                description="A call is already active in this conversation.",
            )

        # CREATE CALL

        call = Call(
            conversation_id=self.conversation_id,
            caller_id=self.user_id,
            receiver_id=receiver.id,
            call_type=self.call_type,
            status=CALL_STATUS_CALLING,
        )

        db.session.add(call)
        db.session.commit()

        return call