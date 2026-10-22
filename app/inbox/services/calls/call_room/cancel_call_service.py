# app/inbox/services/calls/cancel_call_service.py

from datetime import datetime

from flask import abort
from app.inbox.services.settings.blocks.block_policy import BlockPolicy
from app.extensions import db, socketio
from app.inbox.models import Call
from app.inbox.constants.calls import (
    CALL_STATUS_CALLING,
    CALL_STATUS_RINGING,
    CALL_STATUS_CANCELLED,
)
from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)
from app.inbox.services.messages.create_system_message import (
    create_system_message,
)
from app.inbox.serializers.message_serializer import MessageSerializer
from app.inbox.serializers.call_serializer import CallSerializer
from app.models.user import User


class CancelCallService:

    def __init__(
        self,
        call_id: int,
        user_id: int,
    ):
        self.call_id = call_id
        self.user_id = user_id

    def execute(self) -> Call:

        call = Call.query.get(self.call_id)

        if call is None:
            abort(
                404,
                description="Call not found.",
            )

        ConversationGuard.require_participant(
            call.conversation_id,
            self.user_id,
        )

        if call.caller_id != self.user_id:
            abort(
                403,
                description="Only the caller can cancel this call.",
            )
        # BLOCK CHECK

        if BlockPolicy.blocks_either_user(
            call.caller_id,
            call.receiver_id,
        ):
            abort(
                403,
                description="Calling is unavailable.",
            )

        if call.status not in (
            CALL_STATUS_CALLING,
            CALL_STATUS_RINGING,
        ):
            abort(
                409,
                description="Call cannot be cancelled in its current state.",
            )

        call.status = CALL_STATUS_CANCELLED
        call.ended_at = datetime.utcnow()

        cancelled_message = create_system_message(
            conversation_id=call.conversation_id,
            sender_id=call.caller_id,
            event="call_cancelled",
            call_id=call.id,
            call_type=call.call_type,
        )

        db.session.commit()

        socketio.emit(
            "message:new",
            MessageSerializer(cancelled_message).to_dict(),
            room=f"conversation_{call.conversation_id}",
        )

        caller = User.query.get(call.caller_id)

        if caller is None:
            return call

        payload = {
            "call": CallSerializer(call).to_dict(),
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