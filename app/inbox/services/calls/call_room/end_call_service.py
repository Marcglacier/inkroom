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
from app.inbox.services.calls.connections.media_switch_state import (
    media_switch_state,
)
from app.models.user import User
from app.inbox.services.calls.connections.call_connection_state import (
    call_connection_state,
)
from app.inbox.services.messages.create_system_message import (
    create_system_message,
)
from app.inbox.serializers.message_serializer import MessageSerializer


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

        duration_seconds = 0
        
        if call.started_at:
            duration_seconds = max(
                0,
                int(
                    (
                        call.ended_at
                        - call.started_at
                    ).total_seconds()
                ),
            )
        call_message = create_system_message(
            conversation_id=call.conversation_id,
            sender_id=call.caller_id,
            event="call_ended",
            call_id=call.id,
            call_type=call.call_type,
            content=str(duration_seconds),
        )

        db.session.commit()
        socketio.emit(
            "message:new",
            MessageSerializer(call_message).to_dict(),
            room=f"conversation_{call.conversation_id}",
        )
        media_switch_state.clear(call.id)
        
        call_connection_state.clear(call.id)

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